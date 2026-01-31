# Uninstall Helper 🤖

A smart, AI-powered uninstallation tool for Windows, macOS, and Linux that helps you completely remove software with intelligent detection and cleanup.

## ✨ Features

### 🔍 Smart Detection
- **Process Detection**: Find all running processes related to the target software
- **Installation Path Discovery**: Locate files and directories across the system
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

### 🛡️ Safe Uninstallation
- **Multiple Modes**: Safe (detection only), Standard (interactive), Aggressive (full cleanup)
- **Process Termination**: Safely stop running processes before removal
- **File Cleanup**: Remove leftover files and directories
- **System Integration**: Use native package managers when available

### 🤖 AI-Powered Features
- **Intelligent Detection**: Smart pattern matching for software components
- **Conversational Interface**: Interactive mode with user prompts
- **Learning Capabilities**: (Planned) Learn from successful uninstallations
- **Alternative Suggestions**: (Planned) Suggest alternatives to removed software

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Install
```bash
# Clone the repository
git clone https://github.com/ai-openclaw/uninstall-helper.git
cd uninstall-helper

# Install dependencies
pip install -r requirements.txt

# Install as a package (optional)
pip install -e .
```

### Platform-Specific Notes
- **Windows**: No additional requirements
- **macOS**: May require admin privileges for some operations
- **Linux**: Uses native package managers (apt, yum, pacman, etc.)

## 🚀 Usage

### Basic Usage
```bash
# Interactive mode (recommended for beginners)
python main.py

# Uninstall specific software
python main.py "Google Chrome"

# Safe mode (detection only, no changes)
python main.py "Firefox" --safe

# Aggressive mode (full cleanup without prompts)
python main.py "Old Software" --aggressive
```

### Command Line Options
```
usage: main.py [-h] [-i] [-s] [-a] [software]

AI-powered uninstallation tool for Windows, macOS, and Linux

positional arguments:
  software             Name of the software to uninstall

optional arguments:
  -h, --help           show this help message and exit
  -i, --interactive    Run in interactive mode
  -s, --safe           Safe mode (detection only, no changes)
  -a, --aggressive     Aggressive mode (full cleanup without prompts)
```

### Interactive Mode
When running in interactive mode, you'll be guided through:
1. **Software Name**: Enter the name of the software to uninstall
2. **Mode Selection**: Choose between Safe, Standard, or Aggressive modes
3. **Confirmation**: Review and confirm each step before changes are made

## 🔧 How It Works

### 1. Process Detection
- Scans all running processes
- Matches by process name and command line arguments
- Provides option to terminate before uninstallation

### 2. File Discovery
- Searches common installation directories
- Platform-specific path detection
- Identifies related configuration files

### 3. Cleanup Process
- Terminates related processes
- Removes files and directories
- Executes system uninstall commands when available
- Provides detailed summary of actions taken

## 🛠️ Configuration

The tool uses `uninstall_config.json` for platform-specific settings:

### Windows
- Registry uninstall paths
- Program Files directories
- Common application data locations

### macOS
- Applications directory
- Library paths
- User-specific application data

### Linux
- Supported package managers
- Common installation directories
- User-local application paths

## 📁 Project Structure
```
uninstall-helper/
├── main.py              # Main application
├── README.md           # This documentation
├── requirements.txt    # Python dependencies
├── setup.py           # Package installation
├── uninstall_config.json  # Configuration file
└── .git/              # Git repository
```

## 🧪 Testing

### Test on Your System
```bash
# Test detection without making changes
python main.py "python" --safe

# Test interactive mode
python main.py -i
```

### Example Output
```
🔍 Starting uninstallation analysis for: Example Software
📊 System detected: Windows 10

1️⃣  Detecting running processes...
   Found 2 related process(es):
   - PID 1234: example.exe
   - PID 5678: example-helper.exe

2️⃣  Searching for installation paths...
   Found 3 installation path(s):
   - C:\Program Files\Example Software
   - C:\Users\User\AppData\Local\Example
   - C:\ProgramData\Example

3️⃣  Running system uninstall command...
   Command: wmic product where name="Example Software" call uninstall
   ✓ System uninstall completed successfully
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed information
2. **Suggest Features**: Share your ideas for improvement
3. **Submit Code**: Fork the repository and create a pull request
4. **Improve Documentation**: Help make the docs better

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/uninstall-helper.git
cd uninstall-helper

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Use at your own risk!** This tool performs system-level operations that can:
- Remove files and directories
- Terminate running processes
- Execute system commands

Always:
- Backup important data before use
- Review detected items before confirming removal
- Use Safe mode first to see what will be affected
- Have administrator/sudo privileges available

## 🚀 Roadmap

### Short-term Goals
- [x] Basic process detection and termination
- [x] Cross-platform file discovery
- [x] Interactive user interface
- [x] Configuration system

### Medium-term Goals
- [ ] AI-powered pattern recognition
- [ ] Learning from successful uninstallations
- [ ] Backup and restore functionality
- [ ] GUI interface

### Long-term Vision
- [ ] Cloud-based software database
- [ ] Community-driven detection rules
- [ ] Integration with package managers
- [ ] Mobile app companion

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ai-openclaw/uninstall-helper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ai-openclaw/uninstall-helper/discussions)
- **Email**: ai-openclaw@example.com

---

Made with ❤️ by the AI OpenClaw team