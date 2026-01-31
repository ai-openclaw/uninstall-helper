#!/usr/bin/env python3
"""
Uninstall Helper - AI-powered uninstallation tool for Windows, macOS, and Linux.
"""

import psutil
import os
import subprocess
import sys
import json
import platform
import argparse
from pathlib import Path
import shutil

class UninstallHelper:
    def __init__(self):
        self.system = platform.system().lower()
        self.config_file = "uninstall_config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file."""
        default_config = {
            "windows": {
                "uninstall_registry": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                "program_files": ["C:\\Program Files", "C:\\Program Files (x86)"]
            },
            "macos": {
                "applications_dir": "/Applications",
                "library_dir": "~/Library"
            },
            "linux": {
                "package_managers": ["apt", "yum", "dnf", "pacman", "snap", "flatpak"]
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
    
    def detect_processes(self, target_name):
        """
        Detect running processes related to the target software.
        
        Args:
            target_name (str): Name or partial name of the software to detect
        
        Returns:
            list: List of dictionaries with process info
        """
        processes = []
        target_name = target_name.lower()
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                proc_info = proc.info
                # Check process name
                if target_name in proc_info['name'].lower():
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe': proc_info['exe'],
                        'cmdline': proc_info['cmdline']
                    })
                # Check command line arguments
                elif proc_info['cmdline']:
                    cmdline = ' '.join(proc_info['cmdline']).lower()
                    if target_name in cmdline:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'exe': proc_info['exe'],
                            'cmdline': proc_info['cmdline']
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return processes
    
    def terminate_process(self, pid):
        """
        Terminate a process by PID.
        
        Args:
            pid (int): Process ID to terminate
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            print(f"✓ Process terminated: {pid} ({process.name()})")
            return True
        except psutil.NoSuchProcess:
            print(f"✗ Process not found: {pid}")
            return False
        except psutil.AccessDenied:
            print(f"✗ Access denied to terminate process: {pid}")
            return False
        except Exception as e:
            print(f"✗ Failed to terminate process {pid}: {e}")
            return False
    
    def find_installation_paths(self, software_name):
        """
        Find installation paths for the software.
        
        Args:
            software_name (str): Name of the software
        
        Returns:
            list: List of installation paths
        """
        paths = []
        software_name = software_name.lower()
        
        if self.system == "windows":
            # Check Program Files directories
            for prog_dir in self.config.get("windows", {}).get("program_files", []):
                if os.path.exists(prog_dir):
                    for item in os.listdir(prog_dir):
                        if software_name in item.lower():
                            path = os.path.join(prog_dir, item)
                            if os.path.isdir(path):
                                paths.append(path)
        
        elif self.system == "darwin":  # macOS
            apps_dir = self.config.get("macos", {}).get("applications_dir", "/Applications")
            if os.path.exists(apps_dir):
                for item in os.listdir(apps_dir):
                    if software_name in item.lower():
                        path = os.path.join(apps_dir, item)
                        if os.path.isdir(path):
                            paths.append(path)
        
        elif self.system == "linux":
            # Common Linux installation directories
            common_dirs = [
                "/usr/bin",
                "/usr/local/bin",
                "/opt",
                "/snap",
                "/var/lib/flatpak/app"
            ]
            for dir_path in common_dirs:
                if os.path.exists(dir_path):
                    for root, dirs, files in os.walk(dir_path):
                        for item in dirs + files:
                            if software_name in item.lower():
                                path = os.path.join(root, item)
                                paths.append(path)
        
        return paths
    
    def cleanup_files(self, paths):
        """
        Clean up files and directories.
        
        Args:
            paths (list): List of paths to clean up
        
        Returns:
            int: Number of items successfully cleaned up
        """
        cleaned = 0
        
        for path in paths:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"✓ File removed: {path}")
                    cleaned += 1
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✓ Directory removed: {path}")
                    cleaned += 1
            except Exception as e:
                print(f"✗ Failed to remove {path}: {e}")
        
        return cleaned
    
    def get_uninstall_command(self, software_name):
        """
        Get appropriate uninstall command for the system.
        
        Args:
            software_name (str): Name of the software
        
        Returns:
            str: Uninstall command
        """
        if self.system == "windows":
            return f'wmic product where name="{software_name}" call uninstall'
        elif self.system == "darwin":  # macOS
            return f'sudo rm -rf "/Applications/{software_name}.app"'
        elif self.system == "linux":
            # Try to find package manager
            for pm in self.config.get("linux", {}).get("package_managers", []):
                if shutil.which(pm):
                    if pm in ["apt", "apt-get"]:
                        return f'sudo {pm} remove {software_name} -y'
                    elif pm in ["yum", "dnf"]:
                        return f'sudo {pm} remove {software_name} -y'
                    elif pm == "pacman":
                        return f'sudo pacman -R {software_name} --noconfirm'
                    elif pm == "snap":
                        return f'sudo snap remove {software_name}'
                    elif pm == "flatpak":
                        return f'flatpak uninstall {software_name} -y'
            return f'sudo rm -rf /opt/{software_name}'
        
        return ""
    
    def run_uninstall(self, software_name, interactive=False):
        """
        Main uninstallation routine.
        
        Args:
            software_name (str): Name of the software to uninstall
            interactive (bool): Whether to run in interactive mode
        
        Returns:
            dict: Summary of uninstallation results
        """
        print(f"\n🔍 Starting uninstallation analysis for: {software_name}")
        print(f"📊 System detected: {platform.system()} {platform.release()}")
        
        results = {
            "software": software_name,
            "processes_found": 0,
            "processes_terminated": 0,
            "paths_found": 0,
            "paths_cleaned": 0,
            "uninstall_success": False
        }
        
        # Step 1: Detect and terminate processes
        print("\n1️⃣  Detecting running processes...")
        processes = self.detect_processes(software_name)
        results["processes_found"] = len(processes)
        
        if processes:
            print(f"   Found {len(processes)} related process(es):")
            for proc in processes:
                print(f"   - PID {proc['pid']}: {proc['name']}")
            
            if interactive:
                response = input("\n   Terminate these processes? (y/n): ")
                if response.lower() != 'y':
                    print("   Skipping process termination.")
                    return results
            
            print("\n   Terminating processes...")
            for proc in processes:
                if self.terminate_process(proc['pid']):
                    results["processes_terminated"] += 1
        
        # Step 2: Find installation paths
        print("\n2️⃣  Searching for installation paths...")
        paths = self.find_installation_paths(software_name)
        results["paths_found"] = len(paths)
        
        if paths:
            print(f"   Found {len(paths)} installation path(s):")
            for path in paths:
                print(f"   - {path}")
            
            if interactive:
                response = input("\n   Remove these files/directories? (y/n): ")
                if response.lower() != 'y':
                    print("   Skipping file cleanup.")
                else:
                    cleaned = self.cleanup_files(paths)
                    results["paths_cleaned"] = cleaned
            else:
                cleaned = self.cleanup_files(paths)
                results["paths_cleaned"] = cleaned
        
        # Step 3: Run system uninstall command
        print("\n3️⃣  Running system uninstall command...")
        uninstall_cmd = self.get_uninstall_command(software_name)
        
        if uninstall_cmd:
            print(f"   Command: {uninstall_cmd}")
            
            if interactive:
                response = input("\n   Execute this command? (y/n): ")
                if response.lower() != 'y':
                    print("   Skipping system uninstall.")
                    return results
            
            try:
                print("   Executing...")
                result = subprocess.run(
                    uninstall_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print("   ✓ System uninstall completed successfully")
                    results["uninstall_success"] = True
                else:
                    print(f"   ✗ System uninstall failed: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("   ✗ System uninstall timed out")
            except Exception as e:
                print(f"   ✗ Error during system uninstall: {e}")
        else:
            print("   No system-specific uninstall command available")
        
        return results
    
    def interactive_mode(self):
        """Run in interactive mode with user prompts."""
        print("=" * 50)
        print("🤖 Uninstall Helper - Interactive Mode")
        print("=" * 50)
        
        software_name = input("\nEnter the name of the software to uninstall: ").strip()
        
        if not software_name:
            print("No software name provided. Exiting.")
            return
        
        print("\nChoose uninstall mode:")
        print("1. Safe mode (detect only, no changes)")
        print("2. Standard mode (terminate processes, remove files)")
        print("3. Aggressive mode (full cleanup with system uninstall)")
        
        try:
            mode = int(input("\nSelect mode (1-3): "))
        except ValueError:
            mode = 1
        
        if mode == 1:
            # Safe mode - detection only
            processes = self.detect_processes(software_name)
            paths = self.find_installation_paths(software_name)
            
            print(f"\n📊 Detection Results for '{software_name}':")
            print(f"   Processes found: {len(processes)}")
            print(f"   Installation paths found: {len(paths)}")
            
            if processes:
                print("\n   Running processes:")
                for proc in processes:
                    print(f"   - {proc['name']} (PID: {proc['pid']})")
            
            if paths:
                print("\n   Installation paths:")
                for path in paths:
                    print(f"   - {path}")
        
        elif mode == 2:
            # Standard mode
            results = self.run_uninstall(software_name, interactive=True)
            self.print_summary(results)
        
        elif mode == 3:
            # Aggressive mode
            print("\n⚠️  WARNING: Aggressive mode will:")
            print("   - Terminate all related processes")
            print("   - Remove all detected files and directories")
            print("   - Execute system uninstall command")
            
            confirm = input("\nAre you sure you want to continue? (type 'yes' to confirm): ")
            if confirm.lower() == 'yes':
                results = self.run_uninstall(software_name, interactive=False)
                self.print_summary(results)
            else:
                print("Operation cancelled.")
        
        else:
            print("Invalid mode selected.")
    
    def print_summary(self, results):
        """Print a summary of uninstallation results."""
        print("\n" + "=" * 50)
        print("📋 Uninstallation Summary")
        print("=" * 50)
        print(f"Software: {results['software']}")
        print(f"Processes found/terminated: {results['processes_found']}/{results['processes_terminated']}")
        print(f"Paths found/cleaned: {results['paths_found']}/{results['paths_cleaned']}")
        print(f"System uninstall: {'✓ Success' if results['uninstall_success'] else '✗ Failed/Not attempted'}")
        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="AI-powered uninstallation tool for Windows, macOS, and Linux"
    )
    parser.add_argument(
        "software",
        nargs="?",
        help="Name of the software to uninstall"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "-s", "--safe",
        action="store_true",
        help="Safe mode (detection only, no changes)"
    )
    parser.add_argument(
        "-a", "--aggressive",
        action="store_true",
        help="Aggressive mode (full cleanup without prompts)"
    )
    
    args = parser.parse_args()
    helper = UninstallHelper()
    
    if args.interactive or (not args.software and not args.safe and not args.aggressive):
        helper.interactive_mode()
    elif args.software:
        if args.safe:
            # Safe mode - detection only
            processes = helper.detect_processes(args.software)
            paths = helper.find_installation_paths(args.software)
            
            print(f"📊 Detection Results for '{args.software}':")
            print(f"Processes found: {len(processes)}")
            print(f"Installation paths found: {len(paths)}")
            
            if processes:
                print("\nRunning processes:")
                for proc in processes:
                    print(f"- {proc['name']} (PID: {proc['pid']})")
            
            if paths:
                print("\nInstallation paths:")
                for path in paths:
                    print(f"- {path}")
        
        elif args.aggressive:
            # Aggressive mode
            print(f"⚠️  Starting aggressive uninstall for: {args.software}")
            results = helper.run_uninstall(args.software, interactive=False)
            helper.print_summary(results)
        
        else:
            # Standard mode
            results = helper.run_uninstall(args.software, interactive=True)
            helper.print_summary(results)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()