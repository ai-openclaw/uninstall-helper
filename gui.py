#!/usr/bin/env python3
"""
Uninstall Helper GUI - Graphical user interface for the uninstall helper tool.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import sys
import os

class UninstallHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Uninstall Helper GUI")
        self.root.geometry("800x600")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 运行状态
        self.is_running = False
        
        # 权限状态
        self.has_permissions = self.check_permissions()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义颜色
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_bg = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
    
    def check_permissions(self):
        """检查是否有足够的权限"""
        import platform
        system = platform.system().lower()
        
        if system == "linux":
            # 检查是否是root用户
            return os.geteuid() == 0
        elif system == "windows":
            # Windows检查管理员权限
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return True  # 如果检查失败，假设有权限
        else:  # macOS
            return os.geteuid() == 0
    
    def create_widgets(self):
        """创建所有界面组件"""
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="🤖 Uninstall Helper GUI", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 软件名称输入
        ttk.Label(main_frame, text="软件名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.software_entry = ttk.Entry(main_frame, width=40)
        self.software_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 示例按钮
        example_btn = ttk.Button(
            main_frame, 
            text="示例", 
            command=self.fill_example,
            width=8
        )
        example_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # 操作模式选择
        ttk.Label(main_frame, text="操作模式:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.mode_var = tk.StringVar(value="safe")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            mode_frame, 
            text="安全模式 (仅检测)", 
            variable=self.mode_var, 
            value="safe"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            mode_frame, 
            text="标准模式 (交互式)", 
            variable=self.mode_var, 
            value="standard"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            mode_frame, 
            text="激进模式 (全自动)", 
            variable=self.mode_var, 
            value="aggressive"
        ).pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.detect_btn = ttk.Button(
            button_frame,
            text="🔍 开始检测",
            command=self.start_detection,
            width=15
        )
        self.detect_btn.pack(side=tk.LEFT, padx=5)
        
        self.uninstall_btn = ttk.Button(
            button_frame,
            text="🗑️ 开始卸载",
            command=self.start_uninstall,
            width=15
        )
        self.uninstall_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🧹 清空结果",
            command=self.clear_results,
            width=15
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=4, column=0, columnspan=3, pady=(10, 5), sticky=(tk.W, tk.E))
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪", foreground="green")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        # 权限状态显示
        permission_text = "✅ 有管理员权限" if self.has_permissions else "⚠️ 无管理员权限"
        permission_color = "green" if self.has_permissions else "orange"
        self.permission_label = ttk.Label(
            main_frame, 
            text=permission_text, 
            foreground=permission_color,
            font=("Arial", 9)
        )
        self.permission_label.grid(row=5, column=2, sticky=tk.E, pady=(0, 10))
        
        # 结果显示区域
        ttk.Label(main_frame, text="检测结果:").grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        
        # 创建带滚动条的文本区域
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 配置网格权重使文本区域可扩展
        main_frame.rowconfigure(7, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            bg=self.text_bg,
            font=("Consolas", 10)
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 底部信息
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=8, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(
            info_frame,
            text="💡 提示: 安全模式仅检测不执行任何更改",
            foreground="blue"
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            info_frame,
            text=f"Python {sys.version.split()[0]}",
            foreground="gray"
        ).pack(side=tk.RIGHT)
    
    def fill_example(self):
        """填充示例软件名称"""
        examples = ["chrome", "firefox", "python", "vlc", "zoom"]
        import random
        example = random.choice(examples)
        self.software_entry.delete(0, tk.END)
        self.software_entry.insert(0, example)
    
    def start_detection(self):
        """开始检测"""
        software = self.software_entry.get().strip()
        if not software:
            messagebox.showwarning("警告", "请输入软件名称")
            return
        
        self.run_command(software, "safe")
    
    def start_uninstall(self):
        """开始卸载"""
        software = self.software_entry.get().strip()
        if not software:
            messagebox.showwarning("警告", "请输入软件名称")
            return
        
        mode = self.mode_var.get()
        
        # 检查权限（安全模式除外）
        if mode != "safe" and not self.has_permissions:
            import platform
            system = platform.system()
            
            warning_msg = f"⚠️ 权限警告\n\n"
            warning_msg += f"卸载操作需要管理员权限。\n"
            
            if system == "Linux":
                warning_msg += "\n请使用以下方式运行：\n"
                warning_msg += "1. 在终端中运行: sudo python3 run_gui.py\n"
                warning_msg += "2. 或使用安全模式仅进行检测\n"
            elif system == "Windows":
                warning_msg += "\n请以管理员身份运行此程序。\n"
            else:  # macOS
                warning_msg += "\n请使用: sudo python3 run_gui.py\n"
            
            warning_msg += "\n当前将继续执行，但可能会失败。"
            
            if not messagebox.askyesno("权限警告", warning_msg):
                return
        
        if mode == "safe":
            # 安全模式就是检测
            self.run_command(software, "safe")
        elif mode == "standard":
            # 标准模式需要确认
            if messagebox.askyesno("确认", f"确定要卸载 '{software}' 吗？\n\n标准模式会询问每一步操作。"):
                self.run_command(software, "")
        else:  # aggressive
            # 激进模式警告
            if messagebox.askyesno(
                "警告", 
                f"⚠️ 激进模式将自动卸载 '{software}'！\n\n"
                "此模式将：\n"
                "1. 终止所有相关进程\n"
                "2. 删除所有检测到的文件\n"
                "3. 执行系统卸载命令\n\n"
                "确定要继续吗？"
            ):
                self.run_command(software, "aggressive")
    
    def run_command(self, software, mode_flag):
        """运行命令行工具"""
        if self.is_running:
            messagebox.showwarning("警告", "已有任务正在运行")
            return
        
        # 构建命令
        cmd = [sys.executable, "main.py", software]
        if mode_flag == "safe":
            cmd.append("--safe")
        elif mode_flag == "aggressive":
            cmd.append("--aggressive")
        
        # 更新界面状态
        self.is_running = True
        self.detect_btn.config(state="disabled")
        self.uninstall_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="运行中...", foreground="orange")
        
        # 清空之前的结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"正在执行: {' '.join(cmd)}\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # 在新线程中运行命令
        thread = threading.Thread(
            target=self.execute_command,
            args=(cmd, software, mode_flag)
        )
        thread.daemon = True
        thread.start()
    
    def execute_command(self, cmd, software, mode_flag):
        """执行命令并更新界面"""
        try:
            # 执行命令
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 实时读取输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.append_output, output)
            
            # 读取错误输出
            stderr = process.stderr.read()
            if stderr:
                self.root.after(0, self.append_output, f"\n[错误]\n{stderr}\n")
            
            # 获取返回码
            return_code = process.poll()
            
            # 更新界面状态
            self.root.after(0, self.command_finished, return_code, software, mode_flag)
            
        except Exception as e:
            self.root.after(0, self.append_output, f"\n[异常] {str(e)}\n")
            self.root.after(0, self.command_finished, 1, software, mode_flag)
    
    def append_output(self, text):
        """追加输出到文本区域"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.result_text.update_idletasks()
    
    def command_finished(self, return_code, software, mode_flag):
        """命令执行完成"""
        self.is_running = False
        self.detect_btn.config(state="normal")
        self.uninstall_btn.config(state="normal")
        self.progress.stop()
        
        # 显示结果
        if return_code == 0:
            self.status_label.config(text="完成 ✓", foreground="green")
            self.append_output(f"\n{'=' * 60}\n")
            
            if mode_flag == "safe":
                self.append_output(f"✅ '{software}' 检测完成\n")
                self.append_output("安全模式：未执行任何更改\n")
            else:
                self.append_output(f"✅ '{software}' 卸载完成\n")
                
        else:
            self.status_label.config(text="失败 ✗", foreground="red")
            self.append_output(f"\n{'=' * 60}\n")
            self.append_output(f"❌ 操作失败，返回码: {return_code}\n")
        
        self.append_output(f"\n操作已结束。\n")
    
    def clear_results(self):
        """清空结果区域"""
        if self.is_running:
            messagebox.showwarning("警告", "请等待当前任务完成")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="就绪", foreground="green")

def main():
    """主函数"""
    root = tk.Tk()
    app = UninstallHelperGUI(root)
    
    # 处理窗口关闭事件
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel("退出", "有任务正在运行，确定要退出吗？"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()