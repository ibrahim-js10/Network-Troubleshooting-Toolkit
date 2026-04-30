import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import subprocess
import platform
import socket
import threading
from datetime import datetime


class NetworkTroubleshootingToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Network Troubleshooting Toolkit")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        
        # Theme colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eaeaea"
        self.accent_color = "#00d4ff"
        self.secondary_color = "#16213e"
        self.success_color = "#00ff88"
        self.error_color = "#ff4757"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame, 
            text="🔧 Network Troubleshooting Toolkit", 
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=10)
        
        subtitle = tk.Label(
            header_frame,
            text="Professional Network Diagnostics & System Tools",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg="#888888"
        )
        subtitle.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Tools
        left_panel = tk.Frame(content_frame, bg=self.secondary_color, width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Tools Section
        tools_label = tk.Label(
            left_panel,
            text="🛠️ Diagnostic Tools",
            font=("Helvetica", 14, "bold"),
            bg=self.secondary_color,
            fg=self.accent_color
        )
        tools_label.pack(pady=15)
        
        # Target entry
        target_frame = tk.Frame(left_panel, bg=self.secondary_color)
        target_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(
            target_frame,
            text="Target Host/IP:",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg=self.fg_color
        ).pack(anchor=tk.W)
        
        self.target_entry = tk.Entry(
            target_frame,
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT
        )
        self.target_entry.pack(fill=tk.X, pady=5)
        self.target_entry.insert(0, "google.com")
        
        # Tool buttons
        buttons = [
            ("📡 Ping Test", self.run_ping),
            ("🌐 IP Config", self.run_ipconfig),
            ("🔍 Tracert", self.run_tracert),
            ("⚡ DNS Lookup", self.run_nslookup),
            ("🖥️ System Info", self.run_systeminfo),
            ("🔗 Port Scan", self.run_portscan),
            ("📊 Netstat", self.run_netstat),
            ("🧹 Clear Log", self.clear_output),
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                font=("Helvetica", 11, "bold"),
                bg=self.bg_color,
                fg=self.fg_color,
                activebackground=self.accent_color,
                activeforeground=self.bg_color,
                relief=tk.FLAT,
                cursor="hand2",
                command=command,
                height=2
            )
            btn.pack(fill=tk.X, padx=15, pady=3)
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2a2a4e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.bg_color))
        
        # Export button
        export_btn = tk.Button(
            left_panel,
            text="💾 Export Results",
            font=("Helvetica", 12, "bold"),
            bg=self.success_color,
            fg=self.bg_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.export_results,
            height=2
        )
        export_btn.pack(fill=tk.X, padx=15, pady=15)
        
        # Right panel - Output
        right_panel = tk.Frame(content_frame, bg=self.secondary_color)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output header
        output_header = tk.Frame(right_panel, bg=self.secondary_color)
        output_header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            output_header,
            text="📋 Output Console",
            font=("Helvetica", 14, "bold"),
            bg=self.secondary_color,
            fg=self.accent_color
        ).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            output_header,
            text="Ready",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg=self.success_color
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            right_panel,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Footer
        footer = tk.Label(
            self.root,
            text="Network Troubleshooting Toolkit v1.0 | Built with Python & Tkinter",
            font=("Helvetica", 9),
            bg=self.bg_color,
            fg="#666666"
        )
        footer.pack(side=tk.BOTTOM, pady=5)
        
    def log_message(self, message, msg_type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.output_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.output_text.insert(tk.END, f"{message}\n", msg_type)
        
        self.output_text.tag_config("timestamp", foreground="#666666")
        self.output_text.tag_config("info", foreground=self.fg_color)
        self.output_text.tag_config("error", foreground=self.error_color)
        self.output_text.tag_config("success", foreground=self.success_color)
        
        self.output_text.see(tk.END)
        self.root.update()
        
    def run_command(self, command, description):
        self.status_label.config(text=f"Running: {description}", fg=self.accent_color)
        self.progress.start()
        self.log_message(f"Starting {description}...", "info")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True,
                timeout=60
            )
            
            self.progress.stop()
            
            if result.returncode == 0:
                output = result.stdout
                self.log_message(f"✅ {description} completed", "success")
                self.log_message("─" * 50, "info")
                self.log_message(output, "info")
                self.log_message("─" * 50 + "\n", "info")
                self.status_label.config(text="Ready", fg=self.success_color)
                return output
            else:
                error_msg = result.stderr if result.stderr else "Command failed"
                self.log_message(f"❌ Error: {error_msg}", "error")
                self.status_label.config(text="Error", fg=self.error_color)
                return None
                
        except subprocess.TimeoutExpired:
            self.progress.stop()
            self.log_message("⏱️ Command timed out", "error")
            self.status_label.config(text="Timeout", fg=self.error_color)
            return None
        except Exception as e:
            self.progress.stop()
            self.log_message(f"❌ Exception: {str(e)}", "error")
            self.status_label.config(text="Error", fg=self.error_color)
            return None
    
    def run_ping(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target host/IP")
            return
            
        system = platform.system().lower()
        if system == "windows":
            cmd = f"ping -n 4 {target}"
        else:
            cmd = f"ping -c 4 {target}"
            
        self.run_command(cmd, f"Ping Test ({target})")
    
    def run_ipconfig(self):
        system = platform.system().lower()
        if system == "windows":
            cmd = "ipconfig /all"
        else:
            cmd = "ifconfig -a || ip addr"
        self.run_command(cmd, "IP Configuration")
    
    def run_tracert(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target host/IP")
            return
            
        system = platform.system().lower()
        if system == "windows":
            cmd = f"tracert -d {target}"
        else:
            cmd = f"tracert -n {target}"
            
        self.run_command(cmd, f"tracert ({target})")
    
    def run_nslookup(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target host/IP")
            return
        cmd = f"nslookup {target}"
        self.run_command(cmd, f"DNS Lookup ({target})")
    
    def run_systeminfo(self):
        system = platform.system().lower()
        if system == "windows":
            cmd = "systeminfo"
        else:
            cmd = "uname -a && lscpu | head -20"
        self.run_command(cmd, "System Information")
    
    def run_portscan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target host/IP")
            return
            
        self.log_message(f"🔍 Scanning ports on {target}...", "info")
        self.status_label.config(text="Scanning...", fg=self.accent_color)
        self.progress.start()
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    self.log_message(f"  Port {port}: OPEN", "success")
                sock.close()
            except:
                pass
        
        threads = []
        for port in common_ports:
            t = threading.Thread(target=scan_port, args=(port,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        self.progress.stop()
        
        if open_ports:
            self.log_message(f"\n✅ Found {len(open_ports)} open ports", "success")
        else:
            self.log_message(f"\n⚠️ No open ports found", "info")
            
        self.status_label.config(text="Ready", fg=self.success_color)
    
    def run_netstat(self):
        system = platform.system().lower()
        if system == "windows":
            cmd = "netstat -an"
        else:
            cmd = "netstat -tuln"
        self.run_command(cmd, "Network Statistics")
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.log_message("Console cleared", "info")
        self.status_label.config(text="Ready", fg=self.success_color)
    
    def export_results(self):
        content = self.output_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("No Data", "No results to export")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"network_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("=" * 60 + "\n")
                    f.write("NETWORK TROUBLESHOOTING TOOLKIT - EXPORT REPORT\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"System: {platform.system()} {platform.release()}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(content)
                    
                messagebox.showinfo("Success", f"Saved to:\n{filename}")
                self.log_message(f"💾 Exported to {filename}", "success")
            except Exception as e:
                messagebox.showerror("Failed", str(e))
                self.log_message(f"❌ Export failed: {str(e)}", "error")


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTroubleshootingToolkit(root)
    root.mainloop()