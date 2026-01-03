# OCAT Project Structure

## Directory Tree

```
attention-monitor/
│
├── 📄 README.md                          ⭐ Main documentation
├── 📄 SETUP.md                           ⭐ Installation guide
├── 📄 GETTING_STARTED.md                 ⭐ Quick start
├── 📄 CONTRIBUTING.md                    ⭐ Developer guide
├── 📄 CLEANUP_SUMMARY.md                 📋 What we improved
├── 📄 PROJECT_READY.txt                  ✨ Status summary
├── 📄 LICENSE                            📜 MIT License
├── 📄 .gitignore                         🔒 Git ignore rules
├── 📄 requirements.txt                   📦 Root dependencies
│
├── 📁 attention-monitor/                 🎯 MAIN CLIENT
│   ├── 📄 main.py                        ✨ Refactored & documented
│   ├── 📄 facepose.py                    👤 Head pose estimation
│   ├── 📄 hopenet.py                     🧠 Neural network model
│   ├── 📄 utils.py                       🔧 Utility functions
│   ├── 📄 user.py                        👥 User management
│   ├── 📄 testFPS.py                     ⏱️  Performance testing
│   ├── 📄 requirements.txt                📦 Dependencies
│   │
│   ├── 📁 zeromq/                        📡 DATA STREAMING
│   │   ├── 📄 server.py                  ✨ Cleaned & documented
│   │   ├── 📄 client.py                  📨 ZMQ client
│   │   ├── 📄 SerializingContext.py      🔄 Serialization
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 archive/                       📦 OLD CODE
│   │   └── live_plotter.py
│   │
│   ├── 📁 kinesis/                       ☁️  CLOUD STREAMING
│   │   ├── kinesis-producer.py
│   │   ├── kinesis-consumer.py
│   │   └── __init__.py
│   │
│   └── 📁 amv/                           🐍 Virtual environment
│       └── [Python venv files]
│
├── 📁 api/                               🔌 REST API
│   ├── 📄 README.md                      📖 API docs
│   ├── 📄 Dockerfile                     🐳 Docker config
│   └── 📁 app/
│       ├── 📄 main.py                    🌐 Flask server
│       └── 📄 requirements.txt
│
├── 📁 dashboard/                         📊 WEB INTERFACE
│   ├── 📄 package.json                   📦 Node.js config
│   ├── 📄 package-lock.json
│   ├── 📄 jest.config.js                 🧪 Testing config
│   ├── 📄 README.md
│   │
│   ├── 📁 config/
│   │   ├── config.js
│   │   ├── defaultSettings.js
│   │   ├── plugin.config.js
│   │   ├── proxy.js
│   │   └── themePluginConfig.js
│   │
│   ├── 📁 public/                        🎨 Static assets
│   │   ├── favicon.png
│   │   ├── home_bg.png
│   │   └── icons/
│   │
│   ├── 📁 src/                           📝 React source
│   │   ├── global.jsx
│   │   ├── global.less
│   │   ├── manifest.json
│   │   ├── service-worker.js
│   │   ├── assets/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── locales/
│   │   ├── models/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── 📁 tests/
│   │   └── run-tests.js
│   │
│   └── 📁 mock/                          🎭 Mock data
│       ├── notices.js
│       ├── route.js
│       └── user.js
│
├── 📁 model/                             🧠 PRETRAINED MODELS
│   ├── 📄 README.md                      ⭐ Model setup
│   ├── 📄 shape_predictor_68_face_landmarks.dat (⚠️ Download required)
│   └── 📄 put_your_model_here.txt        📝 Instructions
│
├── 📁 realtime_dashboard/                📈 PLOTTING
│   ├── plotter.py
│   ├── server_plotter.py
│   ├── SerializingContext.py
│   └── __pycache__/
│
├── 📁 image/                             🖼️  TEST IMAGES
│   └── lena.jpg
│
├── 📁 cmake-4.2.0/                       🔨 Build tool
│   ├── bin/
│   ├── doc/
│   ├── man/
│   └── share/
│
└── 📄 5fps.gif                           🎬 Demo animation
```

## Module Dependencies

```
attention-monitor/
├── main.py
│   ├── imports: opencv, dlib, torch, zmq, pillow
│   ├── requires: facepose.py, utils.py
│   └── optional: boto3 (AWS Kinesis)
│
├── facepose.py
│   ├── imports: torch, torchvision
│   └── requires: hopenet.py
│
├── utils.py
│   └── imports: opencv, numpy, dlib
│
└── zeromq/
    ├── server.py
    │   └── requires: SerializingContext.py
    └── client.py
        └── requires: SerializingContext.py
```

## File Statistics

| Category | Count | Notes |
|----------|-------|-------|
| **Python Files** | 25+ | Core functionality |
| **Documentation** | 6 | Comprehensive guides |
| **React Components** | 50+ | Dashboard UI |
| **Config Files** | 15+ | Build & deployment |
| **Total Files** | 200+ | Including dependencies |

## Key Locations

### Source Code
- **Client Logic**: `attention-monitor/main.py`
- **API Server**: `api/app/main.py`
- **Data Server**: `attention-monitor/zeromq/server.py`
- **Utilities**: `attention-monitor/utils.py`

### Documentation
- **User Guide**: `README.md`
- **Setup Instructions**: `SETUP.md`
- **Quick Start**: `GETTING_STARTED.md`
- **Developer Guide**: `CONTRIBUTING.md`

### Configuration
- **Python Deps**: `attention-monitor/requirements.txt`
- **Node Deps**: `dashboard/package.json`
- **Git Rules**: `.gitignore`
- **API Config**: `api/Dockerfile`

### Assets
- **Models**: `model/`
- **Images**: `image/`
- **Icons**: `dashboard/public/icons/`
- **Demo**: `5fps.gif`

## Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                      OCAT System                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [Client]              [Server]          [Dashboard]         │
│  attention-monitor     zeromq            dashboard            │
│  └─main.py            └─server.py        └─React App         │
│    ├─facepose.py         |                  |                │
│    ├─utils.py            |                  |                │
│    └─zeromq/client.py    |                  |                │
│                          |                  |                │
│     [Metrics]          [Data]            [Visualization]     │
│     - Blinks           Aggregation       - Charts             │
│     - Yawns            & Storage         - Metrics            │
│     - Yaw/Pitch/Roll   (ZMQ)             - Real-time          │
│                                                               │
│  ┌──────────┐         ┌──────────┐      ┌──────────┐        │
│  │ Webcam   │────────→│ Analysis │─────→│Dashboard │        │
│  └──────────┘         └──────────┘      └──────────┘        │
│                            │                                  │
│                       (Optional)                              │
│                            ↓                                  │
│                       ┌──────────┐                            │
│                       │   API    │                            │
│                       │ Flask    │                            │
│                       └──────────┘                            │
│                            │                                  │
│                       (Optional)                              │
│                            ↓                                  │
│                       ┌──────────┐                            │
│                       │   AWS    │                            │
│                       │ Kinesis  │                            │
│                       └──────────┘                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## File Size Reference

- **main.py**: ~13 KB (refactored)
- **Requirements**: Varies (~2-5 GB installed)
- **Models**: 64 MB (shape_predictor_68_face_landmarks.dat)
- **Dashboard**: ~50 MB (with node_modules)

---

**Structure is now clean and production-ready!** ✨
