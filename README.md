# 🎓 Online Classroom Attention Tracker (OCAT)

> A real-time computer vision system that monitors student attention levels during online classes by tracking eye activity, head pose, and engagement metrics.

[![Demo Video](https://img.shields.io/badge/Demo-Watch%20Video-red?style=for-the-badge)](https://github.com/atomsharan/Attention_monitor)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🎯 Quick Demo

Want to see OCAT in action? Check out these sample recordings:

📹 **Sample Recordings:**
- Location: `C:\Users\Administrator\Videos\Captures\`
- Files can be played back with the system for analysis
- Real-time metrics overlay shows attention tracking

> 💡 **Tip:** Use these recordings to test OCAT without a live webcam!

---

## ✨ Features

- ✅ **📊 Real-time Attention Metrics**: Track blinks, yawns, head pose, and focus loss
- ✅ **👁️ Facial Landmark Detection**: 68-point face landmark detection using dlib
- ✅ **🧠 Head Pose Estimation**: Yaw, pitch, and roll angles for gaze direction
- ✅ **📡 Live Data Streaming**: ZeroMQ-based pub/sub architecture for real-time data
- ✅ **☁️ Cloud Integration**: Optional AWS Kinesis support for data persistence
- ✅ **📈 Interactive Dashboard**: Real-time metrics visualization with PyQtGraph
- ✅ **🌐 Web Dashboard**: React-based dashboard for visualization
- ✅ **📹 Video Playback**: Analyze pre-recorded video files
- ✅ **⚙️ Modular Architecture**: Easy to extend and customize

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

## 🚀 Quick Start (30 seconds)

### Windows Users - One Click Launch
```batch
# Just double-click this file:
START_OCAT.bat
```

### macOS/Linux Users
```bash
# Run the launcher script:
./run-ocat.ps1
```

---

## 📦 Installation

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

## 🎬 Usage

### Option 1: 🎯 Fastest Way (Recommended)

**Windows:**
```batch
# Just run this:
.\START_OCAT.bat
```

**PowerShell:**
```powershell
.\run-ocat.ps1
```

A window will open showing:
- 🎥 Your webcam with facial landmarks
- 📊 Real-time metrics overlay
- 📈 Attention tracking visualization

---

### Option 2: Manual Setup (Advanced)

#### Terminal 1: Start ZeroMQ Server
```bash
cd attention-monitor/zeromq
python server.py
```

Expected output:
```
2026-01-03 18:00:43 - INFO - ZeroMQ Server started on tcp://*:5556
2026-01-03 18:00:43 - INFO - Waiting for client connections...
```

#### Terminal 2: Start Attention Monitor Client
```bash
cd attention-monitor
python main.py --userid student123
```

Expected output:
```
Starting attention monitor for user student123
Connecting to ZeroMQ server at tcp://localhost:5556
```

---

### Option 3: 📺 Play Recorded Video

To test with pre-recorded videos from `C:\Users\Administrator\Videos\Captures\`:

```bash
python main.py --userid test --videofile "C:\Users\Administrator\Videos\Captures\sample.mp4"
```

Or modify `main.py` to load video:
```python
# In main.py, around line 270:
cap = cv2.VideoCapture(r"C:\Users\Administrator\Videos\Captures\sample.mp4")
```

---

### Option 4: 📊 Interactive Dashboard

Start the real-time metrics plotter:

```bash
python realtime_dashboard/plotter.py
```

This opens an interactive dashboard showing:
- 📈 Eye Aspect Ratio (EAR) - blink detection
- 📈 Mouth Aspect Ratio (MAR) - yawn detection
- 📈 Head Pose angles (Yaw/Pitch/Roll)

---

### Option 5: 🌐 Web Dashboard (Optional)

```bash
cd dashboard
npm install
npm start
```

The dashboard will be available at `http://localhost:8000`

---

## ⚙️ Configuration

### Environment Variables

```bash
# Enable AWS Kinesis integration
set ENABLE_KINESIS=1

# Specify camera index (0=default, 1=USB camera, etc.)
set CAM_INDEX=0

# Change ZeroMQ server host
set ZMQ_HOST=192.168.1.100
```

### Custom Thresholds (in `main.py`)

### Custom Thresholds (in `main.py`)

Adjust these values to fine-tune detection sensitivity:

```python
EYE_CLOSED_THRESHOLD = 0.15      # Lower = more sensitive blink detection
YAWN_THRESHOLD = 0.4             # Lower = more sensitive yawn detection  
FOCUS_YAW_THRESHOLD = 30         # Head rotation angle in degrees
```

---

## 📊 Metrics Explained

| Metric | Icon | Description | Range | Alert |
|--------|------|-------------|-------|-------|
| **Blink Count** | 👁️ | Number of eye blinks | Integer | > 60/min = drowsy |
| **Yawn Count** | 😴 | Number of yawning events | Integer | > 3/min = tired |
| **Eye Aspect Ratio (EAR)** | 👀 | Measure of eye openness | 0-1 | < 0.15 = closed |
| **Mouth Aspect Ratio (MAR)** | 👄 | Measure of mouth openness | 0-1 | > 0.4 = yawning |
| **Yaw** | ↔️ | Head horizontal rotation | -90° to +90° | > 30° = looking away |
| **Pitch** | ↕️ | Head vertical rotation | -90° to +90° | < -45° = looking down |
| **Roll** | 🔄 | Head tilt | -90° to +90° | > 30° = unusual angle |
| **Lost Focus Duration** | ⏱️ | Time looking away | Seconds | > 5s = alert |
| **Face Not Present Duration** | ❌ | Time face not detected | Seconds | > 10s = alert |

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

## 🆘 Troubleshooting

### ❌ "Could not open camera"

**Solution:**
```bash
# Try different camera indices
set CAM_INDEX=0
python attention-monitor/main.py --userid test

# Or try index 1
set CAM_INDEX=1
python attention-monitor/main.py --userid test
```

**Debug checklist:**
- ✅ Is your webcam plugged in?
- ✅ Is it being used by another application?
- ✅ Check Device Manager for camera devices

---

### ❌ "dlib compilation error"

**Windows:**
```
Download Visual C++ Build Tools:
https://visualstudio.microsoft.com/downloads/
→ Visual Studio Build Tools 2022
```

**macOS:**
```bash
xcode-select --install
pip install dlib==19.19.0 --no-cache-dir
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-dev build-essential
pip install dlib==19.19.0
```

---

### ❌ "ZeroMQ connection refused"

**Solution:**
```bash
# Check if server is running:
Get-Process python | Where-Object {$_.Name -like "*server*"}

# Check if port 5556 is in use:
netstat -an | grep 5556

# Kill any stuck processes:
Get-Process python | Stop-Process -Force
```

---

### ❌ "ModuleNotFoundError: No module named 'dlib'"

**Solution:**
```bash
# Reinstall with cached wheels:
pip install --upgrade dlib pyzmq opencv-python

# Or use pre-built wheels:
pip install dlib==19.19.0
```

---

### ❌ Plotter window won't appear

**Solution:**
```bash
# Make sure PyQtGraph is installed:
pip install pyqtgraph PyQt5

# Run with verbose output:
python -u realtime_dashboard/plotter.py
```

---

## 🚀 Performance Tips

| Setting | Impact | Recommendation |
|---------|--------|-----------------|
| **Frame Rate** | CPU vs Accuracy | Default 5 FPS (good balance) |
| **Camera Resolution** | CPU vs Detail | 640x480 recommended |
| **Face Detection** | Accuracy | dlib > Haar Cascade |
| **Model Loading** | Startup Speed | ~1-2 seconds first run |

**Optimization tips:**
1. 📊 Lower `FRAME_RATE` from 5 to 3 for slower hardware
2. 📷 Use smaller camera resolution if CPU-bound
3. 🧠 Use OpenCV Haar Cascade if dlib unavailable
4. 💾 Run on SSD for faster model loading

---

## 🎓 Use Cases

- 📚 **Online Education**: Monitor student attention during lectures
- 🎙️ **Presentations**: Track audience engagement in real-time
- 🧠 **User Studies**: Measure attention in psychology research
- 👁️ **Driver Safety**: Detect drowsiness while driving
- 🏥 **Medical**: Monitor patient alertness

---

## 🤝 Contributing

## 🤝 Contributing

We love contributions! Here's how to help:

### Getting Started
1. 🍴 Fork the repository
2. 🌱 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 📝 Make your changes
4. ✅ Test your changes thoroughly
5. 💾 Commit (`git commit -m 'Add amazing feature'`)
6. 📤 Push (`git push origin feature/amazing-feature`)
7. 🔄 Create a Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Add docstrings to functions
- Include unit tests for new features
- Update README for new functionality

### Areas to Contribute
- 🐛 Bug fixes
- ✨ New metrics/features
- 📚 Documentation improvements
- 🚀 Performance optimizations
- 🧪 Additional test coverage

---

## 📄 License

See LICENSE file for details.

## 📞 Support & Resources

### 🆘 Getting Help
- 📋 Check existing [GitHub Issues](https://github.com/atomsharan/Attention_monitor/issues)
- 💬 Start a [Discussion](https://github.com/atomsharan/Attention_monitor/discussions)
- 📧 Email: [Contact Info]

### 📚 Learn More
- [dlib Documentation](http://dlib.net/) - Face detection & landmarks
- [OpenCV Docs](https://docs.opencv.org/) - Computer vision library
- [ZeroMQ Guide](https://zguide.zeromq.org/) - Messaging framework
- [PyTorch Tutorials](https://pytorch.org/tutorials/) - Deep learning
- [Hopenet](https://github.com/natanielruiz/deep-head-pose) - Head pose estimation

### 📖 Academic References
- [PyImageSearch: Facial Landmarks with dlib](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/)
- [PyImageSearch: Drowsiness Detection](https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/)
- [OpenCV: Face Detection](https://docs.opencv.org/master/d7/d8b/tutorial_py_face_detection_in_videos.html)

### 🎥 Sample Videos
Your captured videos are stored in:
```
📁 C:\Users\Administrator\Videos\Captures\
```

Play them back with OCAT for testing:
```bash
python main.py --userid test --videofile "path/to/video.mp4"
```

---

## 👥 Credits & Team

**Original Authors:**
- William Ardianto
- Kenghooi Teoh
- Leonard Loh
- Choo Wilson

**Contributors:**
- Thanks to all community contributors!
- Special thanks to dlib, OpenCV, and PyTorch teams

---

<div align="center">

### ⭐ If you find this project helpful, please give it a star!

[⭐ Star on GitHub](https://github.com/atomsharan/Attention_monitor) | 
[🔗 Report Issue](https://github.com/atomsharan/Attention_monitor/issues) | 
[💬 Start Discussion](https://github.com/atomsharan/Attention_monitor/discussions)

---

Made with ❤️ by the OCAT Team

</div> 
