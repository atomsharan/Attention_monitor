"""
Attention Monitor Client

This module captures video from a webcam and monitors attention-related metrics:
- Eye blinks and blink count
- Yawning and yawn count
- Head pose (yaw, pitch, roll)
- Focus loss (when looking away from screen)
- Face presence duration

The metrics are published via ZeroMQ to a server for real-time visualization.
"""

import argparse
import cv2
import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image
from imutils import face_utils

# Optional dependencies with fallback support
ENABLE_KINESIS = os.getenv('ENABLE_KINESIS', '0') == '1'
if ENABLE_KINESIS:
    import boto3
else:
    boto3 = None

try:
    import dlib
    HAVE_DLIB = True
except ImportError:
    HAVE_DLIB = False

try:
    import zmq
    HAVE_ZMQ = True
except ImportError:
    HAVE_ZMQ = False
    zmq = None

try:
    from facepose import Facepose
    HAVE_FACEPOSE = True
except ImportError:
    HAVE_FACEPOSE = False

from utils import eye_aspect_ratio, mouth_aspect_ratio, rec_to_roi_box, crop_img, draw_axis
from zeromq.SerializingContext import SerializingContext

# ============================================================================
# Configuration
# ============================================================================

# Model paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODEL_PATH = PROJECT_ROOT / "model" / "shape_predictor_68_face_landmarks.dat"

# AWS Configuration (disabled by default)
AWS_REGION = "ap-southeast-1"
KINESIS_STREAM = "kinesis-attention-stream"

# ZeroMQ Configuration
ZMQ_HOST = "localhost"
ZMQ_PORT = 5556

# Frame rate control
FRAME_RATE = 5

# Eye and mouth thresholds
EYE_CLOSED_THRESHOLD = 0.15
YAWN_THRESHOLD = 0.4
FOCUS_YAW_THRESHOLD = 30

# ============================================================================
# Fallback Classes
# ============================================================================

class Dummy:
    """Minimal wrapper to provide .item() method for fallback values"""
    def __init__(self, value):
        self._value = value

    def item(self):
        return self._value


# ============================================================================
# Global Setup
# ============================================================================

# Face detection setup
detector = None
predictor = None
haar_cascade = None

if HAVE_DLIB:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(MODEL_PATH))
else:
    haar_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

# AWS Kinesis setup
kinesis = None
if ENABLE_KINESIS:
    kinesis = boto3.client('kinesis', region_name=AWS_REGION)

# ZeroMQ setup
context = SerializingContext()
socket = context.socket(zmq.PUB) if HAVE_DLIB else None


# ============================================================================
# Camera Management
# ============================================================================

def open_camera():
    """
    Attempt to open a webcam with various backends and indices.
    
    Returns:
        cv2.VideoCapture or None: An opened camera or None if no camera found
    """
    preferred = os.getenv('CAM_INDEX')
    indices = [int(preferred)] if preferred is not None else [0, 1, 2]
    backends = [
        getattr(cv2, 'CAP_DSHOW', 700),
        getattr(cv2, 'CAP_MSMF', 1400),
        getattr(cv2, 'CAP_ANY', 0)
    ]

    for i in indices:
        for b in backends:
            cap = None
            try:
                cap = cv2.VideoCapture(i, b)
            except Exception:
                cap = cv2.VideoCapture(i)
            
            if cap is not None and cap.isOpened():
                return cap
            if cap is not None:
                cap.release()

    return None


# ============================================================================
# Face Detection and Metrics
# ============================================================================

def detect_faces(gray_frame):
    """
    Detect faces in a grayscale frame.
    
    Args:
        gray_frame: Grayscale image
        
    Returns:
        list: Face rectangles/regions
    """
    if HAVE_DLIB:
        return detector(gray_frame, 0)
    else:
        faces = haar_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        ) if haar_cascade is not None else []
        return faces


def get_eye_metrics(shape):
    """
    Calculate eye aspect ratio from facial landmarks.
    
    Args:
        shape: Facial landmarks (68 points)
        
    Returns:
        float: Average eye aspect ratio
    """
    if not HAVE_DLIB:
        return 0.3

    left_eye = shape[36:42]
    right_eye = shape[42:48]
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    return (left_ear + right_ear) / 2.0


def get_mouth_metrics(shape):
    """
    Calculate mouth aspect ratio from facial landmarks.
    
    Args:
        shape: Facial landmarks (68 points)
        
    Returns:
        float: Mouth aspect ratio
    """
    return mouth_aspect_ratio(shape[60:69]) if HAVE_DLIB else 0.1


def get_head_pose(frame, rect, shape=None):
    """
    Estimate head pose (yaw, pitch, roll) from face region.
    
    Args:
        frame: RGB frame
        rect: Face rectangle
        shape: Facial landmarks
        
    Returns:
        tuple: (yaw, pitch, roll) as Dummy objects or actual values
    """
    if not HAVE_FACEPOSE:
        return Dummy(0), Dummy(0), Dummy(0)

    # Extract region of interest
    if HAVE_DLIB:
        roi_box, _, _ = rec_to_roi_box(rect)
        roi_img = crop_img(frame, roi_box)
    else:
        x, y, w, h = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
        roi_img = frame[y0:y1, x0:x1]

    if roi_img.size == 0:
        return Dummy(0), Dummy(0), Dummy(0)

    img = Image.fromarray(roi_img)
    try:
        facepose = Facepose()
        return facepose.predict(img)
    except Exception:
        return Dummy(0), Dummy(0), Dummy(0)


# ============================================================================
# Main Processing Loop
# ============================================================================

def main(userid, host):
    """
    Main attention monitoring loop.
    
    Args:
        userid: User identifier
        host: ZeroMQ server host
    """
    # Connect to ZeroMQ server
    socket.connect(f"tcp://{host}:{ZMQ_PORT}")

    # Open camera
    cap = open_camera()
    if cap is None:
        print("ERROR: Could not open a camera. Try setting CAM_INDEX=0 or 1.")
        return

    # Metrics tracking
    blink_count = 0
    yawn_count = 0
    lost_focus_count = 0
    lost_focus_duration = 0
    face_not_present_duration = 0

    # State tracking
    eye_closed = False
    yawning = False
    lost_focus = False
    focus_timer = None
    face_timer = None

    # Records buffer for Kinesis
    records = []
    last_record = None

    # FPS control
    prev_time = time.time()
    shape = None
    center_x = center_y = 0

    print(f"Starting attention monitor for user {userid}")
    print(f"Connecting to ZeroMQ server at tcp://{host}:{ZMQ_PORT}")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            frame_display = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # FPS control
            time_elapsed = time.time() - prev_time
            if time_elapsed <= 1.0 / FRAME_RATE:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            prev_time = time.time()

            # Detect faces
            rects = detect_faces(gray)

            if len(rects) == 0:
                if face_timer is None:
                    face_timer = time.time()
                face_not_present_duration += time.time() - face_timer
                face_timer = time.time()
            else:
                face_timer = None

            # Process each detected face
            for rect in rects:
                # Get landmarks
                if HAVE_DLIB:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                # Get metrics
                ear = get_eye_metrics(shape) if shape is not None else 0.3
                mar = get_mouth_metrics(shape) if shape is not None else 0.1

                # Blink detection
                if ear < EYE_CLOSED_THRESHOLD:
                    eye_closed = True
                elif ear > EYE_CLOSED_THRESHOLD and eye_closed:
                    blink_count += 1
                    eye_closed = False

                # Yawn detection
                if mar > YAWN_THRESHOLD:
                    yawning = True
                elif mar < YAWN_THRESHOLD * 0.5 and yawning:
                    yawn_count += 1
                    yawning = False

                # Get head pose
                yaw, pitch, roll = get_head_pose(frame, rect, shape)

                # Focus loss detection
                if yaw.item() < -FOCUS_YAW_THRESHOLD or yaw.item() > FOCUS_YAW_THRESHOLD:
                    lost_focus = True
                    if focus_timer is None:
                        focus_timer = time.time()
                    lost_focus_duration += time.time() - focus_timer
                    focus_timer = time.time()
                elif -FOCUS_YAW_THRESHOLD <= yaw.item() <= FOCUS_YAW_THRESHOLD and lost_focus:
                    lost_focus_count += 1
                    lost_focus = False
                    focus_timer = None

                # Create record
                if HAVE_DLIB:
                    center_x = (rect.left() + rect.right()) / 2
                    center_y = (rect.top() + rect.bottom()) / 2
                else:
                    center_x = rect[0] + rect[2] / 2
                    center_y = rect[1] + rect[3] / 2

                last_record = {
                    'id': str(userid),
                    'sortKey': str(uuid.uuid1()),
                    'timestamp': datetime.now().timestamp(),
                    'yaw': yaw.item(),
                    'pitch': pitch.item(),
                    'roll': roll.item(),
                    'ear': ear,
                    'blink_count': blink_count,
                    'mar': mar,
                    'yawn_count': yawn_count,
                    'lost_focus_count': lost_focus_count,
                    'lost_focus_duration': lost_focus_duration,
                    'face_not_present_duration': face_not_present_duration
                }

                # Send to Kinesis if enabled
                if ENABLE_KINESIS:
                    records.append({
                        'Data': bytes(json.dumps(last_record), 'utf-8'),
                        'PartitionKey': str(userid)
                    })
                    if len(records) >= 10:
                        kinesis.put_records(StreamName=KINESIS_STREAM, Records=records)
                        records = []

            # Publish via ZeroMQ
            if last_record is not None:
                data = {'id': str(userid), 'record': last_record}
                frame_stream = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                publish(frame_stream, data)

            # Draw metrics on display frame
            draw_metrics(frame_display, blink_count, yawn_count, lost_focus_count,
                        lost_focus_duration, face_not_present_duration)

            # Draw landmarks and pose if available
            if HAVE_DLIB and shape is not None and len(rects) > 0:
                rect = rects[0]
                draw_border(frame_display, (rect.left(), rect.top()),
                           (rect.left() + rect.width(), rect.top() + rect.height()),
                           (255, 255, 255), 1, 10, 20)
                draw_axis(frame_display, yaw.item(), pitch.item(), roll.item(),
                         tdx=int(center_x), tdy=int(center_y), size=100)
                for idx, (x, y) in enumerate(shape):
                    cv2.circle(frame_display, (x, y), 2, (255, 255, 0), -1)
                    if idx in range(36, 48):  # Eyes
                        cv2.circle(frame_display, (x, y), 2, (255, 0, 255), -1)
                    elif idx in range(60, 68):  # Mouth
                        cv2.circle(frame_display, (x, y), 2, (0, 255, 255), -1)

            cv2.imshow('Attention Monitor', cv2.cvtColor(frame_display, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Attention monitor stopped for user {userid}")


# ============================================================================
# Visualization Helpers
# ============================================================================

def publish(image, data):
    """
    Publish frame and data via ZeroMQ.
    
    Args:
        image: BGR image
        data: Dictionary with metrics
    """
    if image.flags['C_CONTIGUOUS']:
        socket.send_array(image, data, copy=False)
    else:
        image = np.ascontiguousarray(image)
        socket.send_array(image, data, copy=False)


def draw_metrics(frame, blink_count, yawn_count, lost_focus_count,
                lost_focus_duration, face_not_present_duration):
    """Draw attention metrics on frame"""
    y_offset = 20
    metrics = [
        f"Blink Count: {blink_count}",
        f"Yawn Count: {yawn_count}",
        f"Lost Focus Count: {lost_focus_count}",
        f"Lost Focus Duration: {lost_focus_duration:.1f}s",
        f"Face Not Present: {face_not_present_duration:.1f}s"
    ]

    for metric in metrics:
        cv2.putText(frame, metric, (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        y_offset += 20


def draw_border(img, pt1, pt2, color, thickness, r, d):
    """Draw rounded rectangle border on image"""
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Online Classroom Attention Tracker (OCAT) - Client'
    )
    parser.add_argument('--userid', help='User ID', required=True)
    parser.add_argument('--host', help='ZeroMQ server host', default="localhost")

    args = parser.parse_args()

    main(args.userid, args.host)
