# Uninstall Helper 使用示例

## 📖 快速开始

### 1. 安装
```bash
# 克隆仓库
git clone https://github.com/ai-openclaw/uninstall-helper.git
cd uninstall-helper

# 安装依赖
pip install -r requirements.txt
```

### 2. 基本使用
```bash
# 交互式模式（推荐新手）
python main.py -i

# 安全模式检测（不执行任何更改）
python main.py "软件名称" --safe

# 标准卸载模式
python main.py "软件名称"

# 激进模式（无确认提示）
python main.py "软件名称" --aggressive
```

## 🎯 实际示例

### 示例 1：检测 Chrome 浏览器
```bash
# 安全检测 Chrome
python main.py "chrome" --safe

# 输出示例：
# 🔍 Starting uninstallation analysis for: chrome
# 📊 System detected: Windows 10
# 
# 1️⃣  Detecting running processes...
#    Found 3 related process(es):
#    - PID 1234: chrome.exe
#    - PID 5678: chrome.exe
#    - PID 9012: chrome.exe
# 
# 2️⃣  Searching for installation paths...
#    Found 5 installation path(s):
#    - C:\Program Files\Google\Chrome
#    - C:\Users\User\AppData\Local\Google\Chrome
#    - C:\ProgramData\Google\Chrome
# 
# 📋 Detection completed - no changes made (safe mode)
```

### 示例 2：卸载 Python 包
```bash
# 交互式卸载 Python
python main.py "python" -i

# 交互流程：
# 1. 输入软件名称：python
# 2. 选择模式：2 (标准模式)
# 3. 确认进程终止：y
# 4. 确认文件删除：y
# 5. 确认系统卸载：y
```

### 示例 3：清理残留文件
```bash
# 只清理文件，不执行系统卸载
python main.py "old-software"

# 在确认步骤中：
# - 进程终止：y
# - 文件删除：y  
# - 系统卸载：n (跳过)
```

## 🖥️ 平台特定示例

### Windows 系统
```bash
# 使用 Windows 卸载命令
python main.py "Microsoft Edge"

# 生成的命令：
# wmic product where name="Microsoft Edge" call uninstall
```

### macOS 系统
```bash
# 卸载 macOS 应用
python main.py "Safari" --safe

# 检测路径：
# - /Applications/Safari.app
# - ~/Library/Safari
# - ~/Library/Caches/com.apple.Safari
```

### Linux 系统
```bash
# 使用 apt 卸载
python main.py "firefox"

# 生成的命令：
# sudo apt remove firefox -y

# 使用 snap 卸载
python main.py "spotify" --safe
```

## ⚙️ 高级用法

### 批量处理
```bash
# 批量检测多个软件
for software in "chrome" "firefox" "vlc"; do
    echo "检测: $software"
    python main.py "$software" --safe
    echo ""
done
```

### 输出重定向
```bash
# 保存检测结果到文件
python main.py "target-software" --safe > detection_report.txt

# 保存详细日志
python main.py "target-software" 2>&1 | tee uninstall_log.txt
```

### 配置自定义路径
编辑 `uninstall_config.json`：
```json
{
  "windows": {
    "program_files": [
      "C:\\Program Files",
      "C:\\Program Files (x86)",
      "D:\\Programs"  // 添加自定义路径
    ]
  }
}
```

## 🚨 注意事项

### 安全第一
```bash
# 总是先使用安全模式
python main.py "important-software" --safe

# 检查检测结果后再决定
```

### 权限要求
```bash
# Linux/macOS 可能需要 sudo
sudo python main.py "system-software"

# Windows 需要管理员权限
# 以管理员身份运行命令提示符
```

### 备份重要数据
```bash
# 在卸载前备份配置
cp -r ~/.config/software ~/backup/software_config
```

## 🔍 故障排除

### 常见问题

1. **"No processes found"**
   ```bash
   # 软件可能未运行，尝试文件检测
   python main.py "software-name" --safe
   ```

2. **"Access denied"**
   ```bash
   # 提升权限
   sudo python main.py "software-name"
   ```

3. **命令执行失败**
   ```bash
   # 检查系统包管理器
   python main.py "software-name" --safe
   # 查看生成的命令是否正确
   ```

### 调试模式
```bash
# 查看详细输出
python -c "from main import UninstallHelper; h = UninstallHelper(); print(h.system)"
```

## 📊 使用场景

### 场景 1：清理旧版本软件
```bash
# 检测所有 Python 相关文件
python main.py "python2" --safe

# 确认后清理
python main.py "python2"
```

### 场景 2：解决安装问题
```bash
# 完全清理损坏的安装
python main.py "broken-software" --aggressive

# 然后重新安装
```

### 场景 3：系统维护
```bash
# 定期清理测试软件
python main.py "test-app-*" --safe
```

## 🎮 交互模式演示

运行 `python main.py -i` 后的完整交互：

```
🤖 Uninstall Helper - Interactive Mode
==================================================

Enter the name of the software to uninstall: chrome

Choose uninstall mode:
1. Safe mode (detect only, no changes)
2. Standard mode (terminate processes, remove files)
3. Aggressive mode (full cleanup with system uninstall)

Select mode (1-3): 2

🔍 Starting uninstallation analysis for: chrome
📊 System detected: Linux 5.15.0

1️⃣  Detecting running processes...
   Found 2 related process(es):
   - PID 1234: chrome
   - PID 5678: chrome-sandbox

   Terminate these processes? (y/n): y

   Terminating processes...
   ✓ Process terminated: 1234 (chrome)
   ✓ Process terminated: 5678 (chrome-sandbox)

2️⃣  Searching for installation paths...
   Found 3 installation path(s):
   - /opt/google/chrome
   - ~/.config/google-chrome
   - ~/.cache/google-chrome

   Remove these files/directories? (y/n): y
   ✓ Directory removed: /opt/google/chrome
   ✓ Directory removed: /home/user/.config/google-chrome
   ✓ Directory removed: /home/user/.cache/google-chrome

3️⃣  Running system uninstall command...
   Command: sudo apt remove chrome -y
   Execute this command? (y/n): y
   Executing...
   ✓ System uninstall completed successfully

📋 Uninstallation Summary
==================================================
Software: chrome
Processes found/terminated: 2/2
Paths found/cleaned: 3/3
System uninstall: ✓ Success
==================================================
```

## 📝 最佳实践

1. **测试环境先行**：在测试机上先试用
2. **逐步操作**：先安全模式，再标准模式
3. **备份配置**：卸载前备份用户数据
4. **记录操作**：保存卸载日志供参考
5. **验证结果**：卸载后检查系统状态

## 🆘 获取帮助

```bash
# 查看所有选项
python main.py --help

# 查看版本信息
python -c "import main; print('Uninstall Helper v0.1.0')"

# 报告问题
# 访问：https://github.com/ai-openclaw/uninstall-helper/issues
```

---

**提示**：卸载系统关键组件前请务必确认，错误的卸载可能导致系统不稳定。