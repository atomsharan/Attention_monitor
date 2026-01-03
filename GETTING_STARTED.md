# 🚀 Getting Started

Welcome to OCAT! This file will guide you through the next steps.

## Quick Start (5 minutes)

### 1. Download the Model
```bash
# The project needs a facial landmark model
# Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
# Extract and place in model/ folder
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r attention-monitor/requirements.txt
```

### 3. Run in 3 Terminals
```bash
# Terminal 1: Start ZeroMQ Server
cd attention-monitor/zeromq && python server.py

# Terminal 2: Start Client
cd attention-monitor && python main.py --userid alice

# Terminal 3 (Optional): Start Dashboard
cd dashboard && npm install && npm start
```

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed installation guide
- **[README.md](README.md)** - Feature overview and usage
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - What we improved

## 🤔 Common Questions

### Q: How do I monitor attention in real-time?
A: Follow the Quick Start above and press Q in the client window to view metrics.

### Q: Can I use this on multiple computers?
A: Yes! Change `--host` parameter:
```bash
python main.py --userid alice --host 192.168.1.100
```

### Q: What if I don't have dlib?
A: The system automatically falls back to OpenCV (less accurate but works).

### Q: Can I save data to the cloud?
A: Yes! Enable AWS Kinesis:
```bash
export ENABLE_KINESIS=1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
python main.py --userid alice
```

## 🐛 Troubleshooting

### Issue: Camera won't open
```bash
export CAM_INDEX=0
python main.py --userid test
```

### Issue: Import errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r attention-monitor/requirements.txt --force-reinstall
```

### Issue: dlib won't compile
See SETUP.md -> Troubleshooting section

## ✨ Project Highlights

### What Makes OCAT Special

1. **Real-time Processing** - Monitor attention as it happens
2. **Multiple Metrics** - Blinks, yawns, head pose, focus loss
3. **Flexible Architecture** - Works with or without cloud
4. **Open Source** - Fully transparent, community-driven
5. **Well Documented** - Clear code and comprehensive guides

### Features
- ✅ Eye blink detection
- ✅ Yawn detection  
- ✅ Head pose estimation
- ✅ Focus loss tracking
- ✅ Live web dashboard
- ✅ Cloud data storage (optional)

## 🎓 Learning Resources

### Understanding the Code
1. Start with `attention-monitor/main.py` - Main client logic
2. Read `attention-monitor/utils.py` - Helper functions
3. Check `attention-monitor/facepose.py` - Head pose estimation
4. Review `attention-monitor/zeromq/server.py` - Data aggregation

### Key Concepts
- **Eye Aspect Ratio (EAR)**: Measure of eye openness
- **Mouth Aspect Ratio (MAR)**: Measure of mouth openness
- **Head Pose (Yaw/Pitch/Roll)**: Head orientation angles
- **ZeroMQ**: Lightweight messaging for real-time data

## 🤝 Contributing

### Ways to Contribute
1. **Report Bugs** - Found an issue? Open a GitHub issue
2. **Submit Features** - Have an idea? Start a discussion
3. **Improve Code** - Clean up, optimize, document
4. **Enhance Docs** - Fix typos, add examples
5. **Share Feedback** - Tell us what works/doesn't work

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📈 Next Steps

### For Users
- [ ] Complete SETUP.md installation
- [ ] Run Quick Start example
- [ ] Explore the dashboard
- [ ] Read configuration options
- [ ] Try with different users

### For Developers  
- [ ] Fork the repository
- [ ] Read CONTRIBUTING.md
- [ ] Find an issue to work on
- [ ] Submit a pull request

### For Researchers
- [ ] Review the architecture
- [ ] Cite the project
- [ ] Propose research improvements
- [ ] Share findings

## 📞 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yptheangel/attention-monitor/issues)
- 💬 [Discussions](https://github.com/yptheangel/attention-monitor/discussions)
- 📧 Email the maintainers

## 🎉 Success Checklist

Once you're set up:
- [ ] Model file downloaded and placed in `model/` folder
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] ZeroMQ server starts without errors
- [ ] Client runs with webcam input
- [ ] Metrics display in real-time
- [ ] Dashboard loads (optional)

## 🔗 Important Links

- [dlib Face Detection](http://dlib.net/)
- [OpenCV Documentation](https://opencv.org/)
- [ZeroMQ Guide](https://zeromq.org/)
- [PyTorch Tutorials](https://pytorch.org/)

---

**You're all set!** 🎊

Start with SETUP.md and run the Quick Start example above.

Questions? Check the docs or open an issue on GitHub.

Happy monitoring! 👀
