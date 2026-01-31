# Uninstall Helper GUI 使用指南

## 🎯 快速开始

### 1. 启动GUI
```bash
# 方法1: 使用启动脚本（推荐）
python3 run_gui.py

# 方法2: 直接运行
python3 gui.py
```

### 2. 首次运行检查
启动脚本会自动检查并安装所需依赖：
- ✅ Tkinter (Python GUI库)
- ✅ psutil (进程管理库)
- ✅ 主程序文件

## 🖥️ 界面功能说明

### 主界面布局
```
┌─────────────────────────────────────────────────────┐
│                🤖 Uninstall Helper GUI              │
├─────────────────────────────────────────────────────┤
│ 软件名称: [_______________] [示例]                  │
│                                                     │
│ 操作模式: ○ 安全模式 (仅检测)                      │
│          ○ 标准模式 (交互式)                       │
│          ○ 激进模式 (全自动)                       │
│                                                     │
│        [🔍 开始检测] [🗑️ 开始卸载] [🧹 清空结果]   │
│                                                     │
│        [============ 进度条 ============]          │
│                                                     │
│        状态: 就绪                                  │
│                                                     │
│ 检测结果:                                          │
│ ┌──────────────────────────────────────────────┐   │
│ │                                              │   │
│ │  输出区域...                                │   │
│ │                                              │   │
│ └──────────────────────────────────────────────┘   │
│                                                     │
│ 💡 提示: 安全模式仅检测不执行任何更改             │
└─────────────────────────────────────────────────────┘
```

### 功能详解

#### 1. 软件名称输入
- **输入框**: 输入要检测/卸载的软件名称
- **示例按钮**: 随机填充示例软件名（chrome, firefox, python等）

#### 2. 操作模式选择
- **安全模式**: 仅检测，不执行任何更改
- **标准模式**: 交互式，每一步操作前都会询问确认
- **激进模式**: 全自动，无确认直接执行（危险！）

#### 3. 操作按钮
- **🔍 开始检测**: 运行安全模式检测
- **🗑️ 开始卸载**: 根据选择的模式进行卸载
- **🧹 清空结果**: 清空输出区域

#### 4. 状态显示
- **进度条**: 显示操作执行进度
- **状态标签**: 显示当前状态（就绪/运行中/完成/失败）
- **输出区域**: 显示详细的命令行输出

## 🚀 使用示例

### 示例1: 检测Chrome浏览器
1. 在"软件名称"输入框中输入: `chrome`
2. 选择"安全模式"
3. 点击"🔍 开始检测"
4. 查看输出区域中的检测结果

### 示例2: 卸载Firefox
1. 输入: `firefox`
2. 选择"标准模式"
3. 点击"🗑️ 开始卸载"
4. 按照提示确认每一步操作

### 示例3: 快速清理测试软件
1. 输入软件名称
2. 选择"激进模式"
3. 点击"🗑️ 开始卸载"
4. **注意**: 此模式无确认，请谨慎使用！

## ⚙️ 技术细节

### 依赖要求
```bash
# 必需依赖
sudo apt-get install python3-tk
pip install psutil

# 可选依赖（用于高级功能）
pip install pillow  # 图像处理（未来图标支持）
```

### 文件结构
```
uninstall-helper/
├── gui.py              # GUI主程序
├── run_gui.py          # GUI启动器
├── main.py            # 命令行核心逻辑
├── GUI_README.md      # 本文档
└── ...                # 其他项目文件
```

### 工作原理
1. GUI调用命令行工具 `main.py`
2. 实时捕获命令行输出
3. 在图形界面中显示进度和结果
4. 提供友好的交互体验

## 🔧 故障排除

### 常见问题

#### 1. "Tkinter不可用"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install python3-tkinter

# macOS
brew install python-tk
```

#### 2. "psutil未安装"
```bash
pip install psutil
# 或
pip3 install psutil
```

#### 3. GUI窗口不显示
```bash
# 检查显示环境
echo $DISPLAY
# 应该显示 :0 或 :1

# 设置显示（如果需要）
export DISPLAY=:0
```

#### 4. 权限问题
```bash
# 某些操作需要管理员权限
sudo python3 run_gui.py
# 注意：GUI中的某些操作可能仍然需要密码
```

### 调试模式
```bash
# 查看详细错误信息
python3 -c "import gui; gui.main()"

# 检查依赖
python3 run_gui.py
```

## 🎨 自定义配置

### 修改界面样式
编辑 `gui.py` 中的 `setup_styles()` 方法：
```python
def setup_styles(self):
    # 修改颜色
    self.bg_color = "#f5f5f5"      # 背景色
    self.button_color = "#2196F3"  # 按钮颜色
    self.text_bg = "#ffffff"       # 文本背景色
```

### 添加新功能
1. 在 `create_widgets()` 中添加新组件
2. 在 `run_command()` 中扩展命令处理
3. 在 `execute_command()` 中改进输出处理

## 📱 多平台支持

### Windows
```bash
# 安装依赖
pip install psutil
# Tkinter通常随Python一起安装
```

### macOS
```bash
# 安装Tkinter
brew install python-tk

# 安装psutil
pip3 install psutil
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-psutil

# 或分别安装
sudo apt-get install python3-tk
pip3 install psutil
```

## 🔄 与命令行工具集成

### GUI调用命令行
```python
# GUI中的调用方式
cmd = [sys.executable, "main.py", software_name, "--safe"]
subprocess.Popen(cmd, ...)
```

### 保持一致性
- GUI使用与命令行相同的核心逻辑
- 相同的配置文件 (`uninstall_config.json`)
- 相同的错误处理机制
- 相同的输出格式

## 🚧 已知限制

### 当前版本限制
1. **无图标支持**: 窗口使用默认图标
2. **无多语言**: 目前仅支持中文界面
3. **无主题切换**: 固定界面样式
4. **无批量操作**: 一次只能处理一个软件

### 计划改进
- [ ] 添加软件图标支持
- [ ] 多语言界面
- [ ] 暗色/亮色主题
- [ ] 批量卸载功能
- [ ] 历史记录查看
- [ ] 导出报告功能

## 🤝 贡献指南

### 报告问题
1. 描述重现步骤
2. 提供错误信息
3. 说明操作系统和Python版本

### 提交改进
1. Fork项目仓库
2. 创建功能分支
3. 提交Pull Request
4. 包含测试用例

## 📞 支持与反馈

- **问题报告**: GitHub Issues
- **功能建议**: GitHub Discussions
- **紧急支持**: 项目文档

---

**提示**: 首次使用建议先运行"安全模式"了解软件的影响范围，确认无误后再进行实际卸载操作。