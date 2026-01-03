"""
ZeroMQ Server for Attention Monitor

This server:
1. Subscribes to attention metrics from clients
2. Aggregates and processes the data
3. Broadcasts to connected subscribers (dashboards, logging, etc.)
"""

import zmq
import cv2
import logging
from SerializingContext import SerializingContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ZeroMQ Configuration
ZMQ_HOST = "*"
ZMQ_PORT = 5556
ZMQ_PROTOCOL = "tcp"

# Setup context and socket
context = SerializingContext()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b'')
socket.bind(f"{ZMQ_PROTOCOL}://{ZMQ_HOST}:{ZMQ_PORT}")


def subscribe(copy=False):
    """
    Receive OpenCV image and attention metrics.
    
    Arguments:
        copy: (optional) zmq copy flag.
        
    Returns:
        dict: Attention metrics (user ID, yaw, pitch, roll, blink count, etc.)
        ndarray: OpenCV image from client
    """
    msg, image = socket.recv_array(copy=copy)
    return msg, image


def main():
    """
    Main server loop that aggregates and displays client data.
    """
    logger.info(f"ZeroMQ Server started on {ZMQ_PROTOCOL}://{ZMQ_HOST}:{ZMQ_PORT}")
    logger.info("Waiting for client connections...")
    
    try:
        while True:
            try:
                # Receive data from client
                data, image = subscribe()
                
                # Validate data
                if data is None or 'record' not in data:
                    continue
                
                record = data.get('record')
                if record is None:
                    continue
                
                # Log metrics for this frame
                user_id = data.get('id', 'unknown')
                logger.info(
                    f"[{user_id}] "
                    f"Blinks: {record.get('blink_count')}, "
                    f"Yawns: {record.get('yawn_count')}, "
                    f"Yaw: {record.get('yaw'):.1f}°, "
                    f"Lost Focus: {record.get('lost_focus_count')}"
                )
                
                # Display frame with metrics
                if image is not None:
                    cv2.imshow(f"Client: {user_id}", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)
                    
            except Exception as e:
                logger.error(f"Error processing frame: {e}")
                continue
                
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        cv2.destroyAllWindows()
        socket.close()
        context.term()
        logger.info("Server stopped.")


if __name__ == '__main__':
    main()