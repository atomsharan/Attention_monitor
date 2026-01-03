# Contributing to OCAT

We love your input! We want to make contributing to OCAT as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Setup

### Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/attention-monitor.git
cd attention-monitor

# Add upstream remote
git remote add upstream https://github.com/yptheangel/attention-monitor.git
```

### Create Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies with dev tools
pip install -r attention-monitor/requirements.txt
pip install black flake8 pytest
```

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting

```bash
# Format code
black attention-monitor/*.py

# Check style
flake8 attention-monitor/
```

## Making Changes

### Branch Naming

Create a branch with a descriptive name:

```bash
git checkout -b feature/improved-face-detection
# or
git checkout -b bugfix/camera-initialization
# or
git checkout -b docs/add-api-documentation
```

### Commit Messages

Write clear, meaningful commit messages:

```bash
git commit -m "Add head pose estimation improvement

- Improved angle detection accuracy
- Added fallback for missing landmarks
- Reduced computation time by 15%

Fixes #123"
```

### Code Guidelines

1. **Follow PEP 8** style guide
2. **Add docstrings** to functions:
   ```python
   def detect_faces(gray_frame):
       """
       Detect faces in a grayscale frame.
       
       Args:
           gray_frame: Grayscale image
           
       Returns:
           list: Face rectangles/regions
       """
   ```

3. **Handle exceptions gracefully**:
   ```python
   try:
       import dlib
       HAVE_DLIB = True
   except ImportError:
       HAVE_DLIB = False
   ```

4. **Keep functions focused** and under 50 lines when possible
5. **Remove unused imports** and variables
6. **Add type hints** where helpful

## Testing

### Run Tests

```bash
pytest tests/
```

### Write Tests

Create test files in `tests/` directory:

```python
# tests/test_face_detection.py
import pytest
from attention_monitor.utils import eye_aspect_ratio

def test_eye_aspect_ratio():
    # Add test case
    assert eye_aspect_ratio(...) == expected_value
```

## Pull Request Process

1. **Update** the README.md with details of changes if applicable
2. **Follow** the code style guidelines
3. **Include** tests for new features
4. **Document** any configuration changes
5. **Update** version numbers in relevant files

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

## Reporting Bugs

Use the GitHub Issues template:

### Include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**:
   ```
   1. Run `python main.py --userid test123`
   2. Move face away from camera
   3. ...
   ```
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Python version
   - dlib installed? (Y/N)
6. **Screenshots/Logs**: Attach error messages or screenshots

## Suggesting Enhancements

Describe:
1. **Current Behavior**: How it works now
2. **Desired Behavior**: What you'd like to see
3. **Use Case**: Why this would be useful
4. **Possible Implementation**: Your ideas (optional)

## Code Review

Maintainers will review your PR for:
- ✅ Code quality and style
- ✅ Test coverage
- ✅ Documentation
- ✅ Performance impact
- ✅ Security concerns

Be open to feedback and suggestions!

## Becoming a Maintainer

Active contributors who consistently provide quality improvements may be invited to become maintainers. This includes:

- Triaging issues
- Reviewing pull requests
- Merging approved changes
- Managing releases

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Questions?

- 📧 Email the maintainers
- 💬 Start a GitHub Discussion
- 🐛 Open an Issue for questions/clarifications

## Community Guidelines

Please note we have a code of conduct. Follow it in all interactions:

- Be respectful and inclusive
- No harassment or discrimination
- Assume good intent
- Help others learn and grow

---

**Thank you for contributing to OCAT!** 🎉
