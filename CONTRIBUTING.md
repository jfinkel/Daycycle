# Contributing to Daycycle

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to Daycycle.

## Ways to Contribute

- 🐛 **Report bugs** - Found an issue? Open a GitHub issue
- ✨ **Suggest features** - Have an idea? Discuss it in issues
- 📝 **Improve documentation** - Typos, clarity, examples
- 💻 **Submit code** - Bug fixes, new features, optimizations
- 🎨 **Design** - UI/UX improvements, icons, screenshots
- 🧪 **Testing** - Test on different systems and report results

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/jfinkel/daycycle.git
cd daycycle
```

### 2. Set Up Development Environment

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt  # if it exists, otherwise:
pip install Pillow
pip install tkinterdnd2
```

### 3. Make Your Changes

- Create a new branch: `git checkout -b feature/your-feature-name`
- Make your changes
- Test thoroughly

### 4. Submit a Pull Request

- Push to your fork
- Open a pull request with clear description
- Reference any related issues (#123)

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where helpful
- Add docstrings to functions
- Keep lines under 100 characters

### Commit Messages

Format: `Type: Brief description`

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (no functional changes)
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

Examples:
```
feat: Add keyboard shortcuts to settings UI
fix: Correct sunrise calculation for southern hemisphere
docs: Update installation instructions for Fedora
```

### Testing

Before submitting:
1. Test on multiple Python versions (3.9, 3.10, 3.11, 3.12)
2. Test with and without optional dependencies
3. Test on different Linux distributions if possible
4. Run manual tests on your system

### File Organization

```
daycycle/
├── daycycle-wallpaper.sh      # Main wallpaper update script
├── daycycle-settings.py       # Settings GUI
├── daycycle-config.sh         # Config script launcher
├── daycycle-install.sh        # Installation script
├── daycycle-wallpaper.service # Systemd service
├── daycycle-wallpaper.timer   # Systemd timer
├── README.md                  # Project overview
├── USAGE.md                   # Usage documentation
├── CONTRIBUTING.md            # This file
└── LICENSE                    # MIT License
```

## Feature Development

### Before Starting

1. Check existing issues - maybe it's already being worked on
2. Open an issue to discuss major changes first
3. Get feedback from maintainers

### Process

1. Create a feature branch: `git checkout -b feature/descriptive-name`
2. Make focused, logical commits
3. Add comments for complex logic
4. Test thoroughly
5. Update documentation if needed
6. Submit PR with clear description

### Feature Ideas Under Discussion

- [ ] Support for multiple monitors
- [ ] Smooth fade transitions between wallpapers
- [ ] Integration with music/activity detection
- [ ] Custom time rules and scheduling
- [ ] Wallpaper collection management
- [ ] Support for other display managers

Feel free to work on any of these!

## Bug Reporting

### Before Reporting

- Check existing issues - maybe it's already reported
- Try the latest version
- Try without optional dependencies

### Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**System Info**
- OS: Ubuntu 22.04 / Fedora 37 / Arch Linux
- Python version: 3.10
- Display: Wayland / X11
- Desktop: GNOME / KDE / XFCE

**Steps to Reproduce**
1. Configure daycycle with...
2. Set images to...
3. See error...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Logs**
```
journalctl --user -u daycycle-wallpaper.service
```

**Screenshots**
If applicable

**Additional Context**
Any other context
```

## Documentation

### Updating Docs

- Edit README.md for overview changes
- Edit USAGE.md for usage/tutorial updates
- Add comments in code for complex logic
- Update this file for contribution process changes

### Documentation Standards

- Clear, concise language
- Use examples where helpful
- Include command syntax
- Add troubleshooting sections
- Link to relevant sections

## Code Review

### What We Look For

- ✅ Follows PEP 8 style guide
- ✅ Has clear commit messages
- ✅ Includes relevant tests/verification
- ✅ Updates documentation if needed
- ✅ No unnecessary dependencies
- ✅ Handles edge cases gracefully
- ✅ Works with optional dependencies disabled

### Review Feedback

- Be respectful and constructive
- Explain reasoning behind suggestions
- Ask questions to understand intent
- Approve when satisfied

## Maintenance Notes

### Key Files to Understand

**daycycle-wallpaper.sh**
- Reads config from `~/.config/daycycle-wallpaper.conf`
- Calculates sunrise/sunset using astral library
- Sets wallpaper using `feh` or similar
- Runs via systemd timer every 15 minutes

**daycycle-settings.py**
- Tkinter GUI for configuration
- Reads/writes config file
- Provides image preview with PIL
- Supports drag-and-drop with tkinterdnd2

**daycycle-install.sh**
- Checks dependencies
- Installs optional packages
- Sets up systemd units
- Creates necessary directories

### Testing Different Scenarios

```bash
# Test without PIL (no thumbnails)
# Uninstall or mock in test environment

# Test without tkinterdnd2 (no drag-drop)
# Comment out DND imports

# Test on different timezones
TZ=Europe/London daycycle-wallpaper.sh
TZ=Asia/Tokyo daycycle-wallpaper.sh

# Test different display managers
# XFCE, GNOME, KDE, etc. have different wallpaper commands
```

## Release Process

Maintainers only:

1. Update version in scripts
2. Update CHANGELOG.md
3. Create tag: `git tag v1.0.0`
4. Push tag: `git push --tags`
5. Create GitHub release
6. Write release notes

## Community

- Be respectful and inclusive
- Assume good intent
- Help others who are starting out
- Share ideas and feedback
- Celebrate contributions!

## Questions?

- Check README.md and USAGE.md
- Search existing issues
- Open a new issue with `question:` prefix
- Contact maintainers

## License

By contributing, you agree your code will be licensed under the MIT License (same as the project).

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Project acknowledgments section
- Release notes (for significant contributions)

Thank you for making Daycycle better! 🌅
