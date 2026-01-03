# OCAT Setup Guide

Complete setup instructions for Online Classroom Attention Tracker.

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.6 - 3.9 (3.10+ may have compatibility issues with older packages)
- **RAM**: 4GB minimum (8GB recommended)
- **Webcam**: USB or built-in camera
- **GPU** (optional): NVIDIA GPU with CUDA for faster processing

## Step-by-Step Installation

### 1. Clone Repository

```bash
git clone https://github.com/yptheangel/attention-monitor.git
cd attention-monitor
```

### 2. Download Face Landmark Model

Download the dlib face landmark predictor model:

```bash
# Option 1: Manual download
# Visit: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
# Extract and place in model/ directory

# Option 2: Using wget (Linux/macOS)
cd model
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
cd ..

# Option 3: Using PowerShell (Windows)
# cd model
# Invoke-WebRequest -Uri "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2" -OutFile "shape_predictor_68_face_landmarks.dat.bz2"
# 7z x shape_predictor_68_face_landmarks.dat.bz2
# cd ..
```

Verify the file:
```bash
ls model/shape_predictor_68_face_landmarks.dat
```

### 3. Create Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r attention-monitor/requirements.txt

# Optional: Install API dependencies
pip install flask flask-cors boto3 pandas

# Optional: Install dashboard dependencies (Node.js required)
cd dashboard
npm install
cd ..
```

### 5. Verify Installation

```bash
python -c "import dlib; import cv2; import torch; print('✓ All dependencies installed')"
```

## Running the Application

### Terminal 1: ZeroMQ Server

```bash
cd attention-monitor/zeromq
python server.py
```

Expected output:
```
Binding to tcp://*:5556
Waiting for connections...
```

### Terminal 2: Attention Monitor Client

```bash
cd attention-monitor
python main.py --userid alice
```

Replace `alice` with your user ID. The client will:
- Open your webcam
- Display real-time metrics
- Stream data to the ZeroMQ server

### Terminal 3: Optional - API Server

```bash
cd api/app
python main.py
```

API will be available at `http://localhost:80`

### Terminal 4: Optional - Web Dashboard

```bash
cd dashboard
npm start
```

Dashboard will open at `http://localhost:8000`

## Configuration

### Camera Selection

If your system has multiple cameras:

```bash
export CAM_INDEX=0  # or 1, 2, etc.
python main.py --userid alice
```

### AWS Kinesis Integration

To enable cloud data storage:

```bash
export ENABLE_KINESIS=1
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

python main.py --userid alice
```

### Custom ZeroMQ Port

Edit `attention-monitor/main.py` and change:
```python
ZMQ_PORT = 5556  # Change this
```

Also update the server in `attention-monitor/zeromq/server.py`

## Troubleshooting

### Issue: Camera won't open

```bash
# List available cameras
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"

# Try different camera index
export CAM_INDEX=1
python main.py --userid test
```

### Issue: dlib compilation fails

**Windows:**
- Download Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
- Install "Desktop development with C++"

**macOS:**
```bash
xcode-select --install
```

**Linux (Ubuntu):**
```bash
sudo apt-get install python3-dev build-essential
```

### Issue: ModuleNotFoundError

Ensure virtual environment is activated:

```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

Then reinstall dependencies:
```bash
pip install -r attention-monitor/requirements.txt
```

### Issue: ZeroMQ connection refused

Ensure the server is running in a separate terminal:
```bash
# Terminal 1
cd attention-monitor/zeromq
python server.py

# Then in Terminal 2
cd attention-monitor
python main.py --userid alice
```

### Issue: Webcam shows but no face detected

- Ensure good lighting
- Position face directly in front of camera
- Face should be at least 60x60 pixels
- Try adjusting camera distance

## Performance Optimization

### Reduce CPU Usage

```python
# Edit attention-monitor/main.py
FRAME_RATE = 3  # Lower from 5 to 3 FPS
```

### Use OpenCV Instead of dlib

The system automatically falls back to OpenCV if dlib is unavailable. While less accurate, it's faster.

### GPU Acceleration (optional)

For PyTorch GPU support:
```bash
# For NVIDIA CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Next Steps

1. Read the [README.md](README.md) for usage details
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
3. Join the discussions on GitHub Issues

## Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yptheangel/attention-monitor/issues)
- 💬 [Discussions](https://github.com/yptheangel/attention-monitor/discussions)

---

**Happy monitoring!** 👀
