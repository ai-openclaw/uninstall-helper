#!/usr/bin/env python3
"""
启动Uninstall Helper GUI的脚本
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    # 检查tkinter
    try:
        import tkinter
        print("✅ Tkinter 可用")
    except ImportError:
        print("❌ Tkinter 不可用，请安装: sudo apt-get install python3-tk")
        return False
    
    # 检查psutil
    try:
        import psutil
        print("✅ psutil 可用")
    except ImportError:
        print("⚠️  psutil 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("✅ psutil 安装成功")
        except:
            print("❌ psutil 安装失败，请手动安装: pip install psutil")
            return False
    
    # 检查主程序
    if not os.path.exists("main.py"):
        print("❌ 找不到 main.py")
        return False
    
    print("✅ 所有依赖检查通过")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 Uninstall Helper GUI 启动器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，无法启动GUI")
        input("按Enter键退出...")
        return
    
    # 启动GUI
    print("\n🚀 启动GUI...")
    try:
        # 切换到当前目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # 导入并运行GUI
        from gui import main as gui_main
        gui_main()
        
    except Exception as e:
        print(f"\n❌ GUI启动失败: {e}")
        print("\n尝试手动启动:")
        print("1. cd /home/admin/clawd/uninstall-helper")
        print("2. python3 gui.py")
        input("\n按Enter键退出...")

if __name__ == "__main__":
    main()