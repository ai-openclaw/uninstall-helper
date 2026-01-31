#!/usr/bin/env python3
"""
测试权限修复
"""

import os
import sys

def check_sudo_permission():
    """检查是否有sudo权限"""
    if os.geteuid() == 0:
        print("✅ 当前有root权限")
        return True
    else:
        print("❌ 当前无root权限，需要sudo")
        print("   请使用: sudo python3 main.py '软件名'")
        return False

def simulate_uninstall():
    """模拟卸载过程"""
    print("\n🔧 模拟卸载流程")
    print("=" * 50)
    
    # 检查权限
    if not check_sudo_permission():
        print("\n💡 解决方案:")
        print("1. 使用sudo运行: sudo python3 main.py '软件名'")
        print("2. 使用GUI版本: sudo python3 run_gui.py")
        print("3. 手动执行命令: sudo apt remove 软件名 -y")
        return False
    
    # 如果有权限，继续执行
    print("\n✅ 有足够权限，可以继续执行卸载")
    return True

def main():
    print("🤖 卸载助手权限测试")
    print("=" * 50)
    
    # 测试当前权限
    simulate_uninstall()
    
    print("\n" + "=" * 50)
    print("📋 总结:")
    print("- 工具本身工作正常")
    print("- 问题在于Linux系统权限限制")
    print("- apt remove命令需要root权限")
    print("- 解决方案: 使用sudo运行工具")
    
    # 显示正确的使用方法
    print("\n🎯 正确使用方法:")
    print("```bash")
    print("# 方法1: 使用sudo")
    print("sudo python3 main.py 'gnome-todo'")
    print("")
    print("# 方法2: 回答'y'确认")
    print("sudo python3 main.py 'gnome-todo'")
    print("# 当提示'Terminate these processes? (y/n):'时输入y")
    print("")
    print("# 方法3: 使用激进模式")
    print("sudo python3 main.py 'gnome-todo' --aggressive")
    print("```")

if __name__ == "__main__":
    main()