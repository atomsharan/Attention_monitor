# Online Classroom Attention Tracker (OCAT)

A real-time computer vision system that monitors student attention levels during online classes by tracking eye activity, head pose, and engagement metrics.

![Online Class Attention Tracker](5fps.gif "Online Class Attention Tracker")

## Features

- ✅ **Real-time Attention Metrics**: Track blinks, yawns, head pose, and focus loss
- ✅ **Facial Landmark Detection**: 68-point face landmark detection using dlib
- ✅ **Head Pose Estimation**: Yaw, pitch, and roll angles for gaze direction
- ✅ **Live Data Streaming**: ZeroMQ-based pub/sub architecture for real-time data
- ✅ **Cloud Integration**: Optional AWS Kinesis support for data persistence
- ✅ **Web Dashboard**: React-based dashboard for visualization
- ✅ **Responsive UI**: Ant Design Pro framework

## System Architecture

```
┌─────────────────────┐
│  Client (Python)    │
│  - Video Capture    │
│  - Face Detection   │
│  - Metrics Calc     │
└──────────┬──────────┘
           │ ZeroMQ PUB
           ▼
┌──────────────────────┐
│  ZeroMQ Server      │
│  - Data Aggregation │
│  - Broadcasting     │
└──────────┬──────────┘
           │ ZeroMQ SUB
           ▼
┌──────────────────────┐
│  Dashboard (React)   │
│  - Real-time Charts │
│  - Metrics Display   │
└─────────────────────┘
```

## Installation

### Prerequisites

- Python 3.6+ 
- Webcam/USB camera
- 4GB RAM minimum

### Step 1: Download Face Landmark Model

The project requires the dlib face landmark predictor model:

1. Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
2. Extract the `.bz2` file
3. Place `shape_predictor_68_face_landmarks.dat` in the `model/` directory

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r attention-monitor/requirements.txt
```

### Step 3: Install Dashboard Dependencies (Optional)

```bash
cd dashboard
npm install
```

## Usage

### Start ZeroMQ Server

```bash
cd attention-monitor/zeromq
python server.py
```

The server will bind to `tcp://*:5556` and wait for client connections.

### Start Attention Monitor Client

```bash
cd attention-monitor
python main.py --userid <user_id> [--host <server_host>]
```

**Arguments:**
- `--userid`: Unique identifier for the user (required)
- `--host`: ZeroMQ server hostname (default: localhost)

**Examples:**
```bash
python main.py --userid student123
python main.py --userid alice --host 192.168.1.100
```

### Optional: Start Flask API Server

The API server processes and exposes attention metrics via REST endpoints:

```bash
cd api/app
python main.py
```

The API will run on `http://localhost:80`

### Optional: Start Web Dashboard

```bash
cd dashboard
npm start
```

The dashboard will be available at `http://localhost:8000`

## Configuration

### Environment Variables

```bash
# Enable AWS Kinesis integration
export ENABLE_KINESIS=1

# Specify camera index (0=default)
export CAM_INDEX=0
```

## Metrics Explained

| Metric | Description | Range |
|--------|-------------|-------|
| **Blink Count** | Number of eye blinks | Integer |
| **Yawn Count** | Number of yawning events | Integer |
| **Eye Aspect Ratio (EAR)** | Measure of eye openness | 0-1 |
| **Mouth Aspect Ratio (MAR)** | Measure of mouth openness | 0-1 |
| **Yaw** | Head horizontal rotation | -90° to +90° |
| **Pitch** | Head vertical rotation | -90° to +90° |
| **Roll** | Head tilt | -90° to +90° |
| **Lost Focus Duration** | Time looking away | Seconds |
| **Face Not Present Duration** | Time face not detected | Seconds |

## Project Structure

```
attention-monitor/
├── attention-monitor/          # Client application
│   ├── main.py                 # Main attention monitoring client
│   ├── facepose.py            # Head pose estimation
│   ├── utils.py               # Utility functions
│   ├── user.py                # User management
│   ├── zeromq/                # ZeroMQ client/server
│   └── requirements.txt        # Python dependencies
├── api/                        # Flask REST API
│   ├── app/
│   │   └── main.py            # Flask application
│   └── Dockerfile             # Docker configuration
├── dashboard/                  # React web dashboard
│   ├── src/                   # React source code
│   ├── package.json           # Node dependencies
│   └── config/                # Webpack configuration
├── model/                      # Pre-trained models
│   └── README.md              # Model setup instructions
└── README.md                   # This file
```

## Troubleshooting

### Issue: "Could not open camera"
```bash
# Try specifying camera index
export CAM_INDEX=0
python main.py --userid test123
```

### Issue: dlib compilation error
```bash
# Install build tools
# Windows: Download Visual C++ Build Tools
# macOS: xcode-select --install
# Linux: sudo apt-get install python3-dev build-essential
```

### Issue: ZeroMQ connection refused
```bash
# Ensure server is running in separate terminal
# Check if port 5556 is in use:
netstat -an | grep 5556
```

## Performance Tips

1. **Frame Rate Control**: Default is 5 FPS for balance between accuracy and CPU usage
2. **Camera Resolution**: Lower resolution = faster processing but less accurate
3. **Model Accuracy**: dlib offers better accuracy than OpenCV Haar Cascades

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

See LICENSE file for details.

## Contributors

- William Ardianto
- Kenghooi Teoh
- Leonard Loh
- Choo Wilson

## References

- [dlib Face Detection](http://dlib.net/)
- [OpenCV Computer Vision](https://opencv.org/)
- [ZeroMQ Messaging](https://zeromq.org/)
- [PyTorch Deep Learning](https://pytorch.org/)
- [Hopenet Head Pose Estimation](https://github.com/natanielruiz/deep-head-pose)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
- [PyImageSearch](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/) Facial landmarks with dlib, OpenCV, and Python
- [PyImageSearch](https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/) Drowsiness detection with OpenCV 
