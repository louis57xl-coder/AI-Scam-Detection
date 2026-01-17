import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, END, NORMAL, DISABLED
from tkinter import ttk
import threading
import re

# --- AUTOMATIC REPAIR ---
try:
    from google import genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "google-genai"])
    from google import genai

class ScamCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScamScanner Pro - Gemini 2.5")
        self.root.geometry("1100x950") 

        # --- TOP API KEY SECTION ---
        api_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
        api_frame.pack(fill=tk.X)
        
        tk.Label(api_frame, text="Gemini API Key:", font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=(20, 10))
        self.api_entry = tk.Entry(api_frame, font=("Consolas", 10), width=50)
        self.api_entry.pack(side=tk.LEFT, padx=5)
        
        # --- TOP BOX RIGHT-CLICK MENU ---
        self.api_menu = Menu(self.api_entry, tearoff=0)
        self.api_menu.add_command(label="Cut", command=lambda: self.api_entry.event_generate("<<Cut>>"))
        self.api_menu.add_command(label="Copy", command=lambda: self.api_entry.event_generate("<<Copy>>"))
        self.api_menu.add_command(label="Paste", command=lambda: self.api_entry.event_generate("<<Paste>>"))
        self.api_entry.bind("<Button-3>", lambda e: self.api_menu.tk_popup(e.x_root, e.y_root))
        
        tk.Button(api_frame, text="Apply & Save Key", command=self.apply_key, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)

        self.client = None
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=5)

        # --- UI ELEMENTS ---
        tk.Label(root, text="Analysis Dashboard", font=("Segoe UI", 12, "bold")).pack(pady=5, padx=20, anchor="w")
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=22, font=("Consolas", 11), state=DISABLED)
        self.result_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        self.result_text.tag_config("high", foreground="red", font=("Consolas", 16, "bold"))
        self.result_text.tag_config("med", foreground="orange", font=("Consolas", 16, "bold"))

        tk.Label(root, text="Input Message (Right-Click to Paste):", font=("Segoe UI", 11, "bold")).pack(pady=5, padx=20, anchor="w")
        
        # --- BOTTOM INPUT BOX ---
        self.input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=12, font=("Consolas", 11))
        self.input_text.pack(padx=20, pady=5, fill=tk.BOTH)

        # --- BOTTOM BOX RIGHT-CLICK MENU (FIXED) ---
        self.msg_menu = Menu(self.input_text, tearoff=0)
        self.msg_menu.add_command(label="Cut", command=lambda: self.input_text.event_generate("<<Cut>>"))
        self.msg_menu.add_command(label="Copy", command=lambda: self.input_text.event_generate("<<Copy>>"))
        self.msg_menu.add_command(label="Paste", command=lambda: self.input_text.event_generate("<<Paste>>"))
        self.msg_menu.add_separator()
        self.msg_menu.add_command(label="Select All", command=lambda: self.input_text.tag_add("sel", "1.0", END))
        
        # This binds the right-click event to the bottom window
        self.input_text.bind("<Button-3>", lambda e: self.msg_menu.tk_popup(e.x_root, e.y_root))

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.scan_btn = tk.Button(btn_frame, text="START DEEP SCAN", command=self.start_scan, bg="#4CAF50", fg="white", width=30, font=("Segoe UI", 12, "bold"))
        self.scan_btn.pack()

    def apply_key(self):
        key = self.api_entry.get().strip()
        if not key:
            messagebox.showwarning("Key Error", "Please paste your Gemini API key.")
            return False
        try:
            self.client = genai.Client(api_key=key)
            messagebox.showinfo("Success", "API Key connected successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))
            return False

    def start_scan(self):
        msg = self.input_text.get("1.0", END).strip()
        if not msg: return
        if self.client is None and not self.apply_key(): return

        self.scan_btn.config(state=DISABLED, text="SCANNING...")
        self.progress.start(10)
        
        self.result_text.configure(state=NORMAL)
        self.result_text.insert(END, "\n" + "-"*60 + "\nAI IS SEARCHING FOR SCAM INDICATORS...\n" + "-"*60 + "\n")
        self.result_text.configure(state=DISABLED)
        
        threading.Thread(target=self.do_gemini, args=(msg,), daemon=True).start()

    def do_gemini(self, text):
        try:
            prompt = f"""SYSTEM ROLE: You are a Cybersecurity Fraud Expert.
            Analyze the text for scams. Be extremely critical. 
            Minor suspicious patterns must result in a higher score.
            
            OUTPUT FORMAT:
            [SCORE: X/100]
            REASONING: (Detailed analysis)
            
            TEXT: {text}"""
            
            response = self.client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
            output = response.text.strip()
            
            score = 0
            match = re.search(r"SCORE:\s*(\d+)", output, re.IGNORECASE)
            if match: score = int(match.group(1))
            
            tag = ""
            if score >= 70: tag = "high"
            elif score >= 30: tag = "med"

            def update_ui():
                self.progress.stop()
                self.scan_btn.config(state=NORMAL, text="START DEEP SCAN")
                self.result_text.configure(state=NORMAL)
                self.result_text.insert(END, f"SCAM RISK RATING: {score}%\n", tag)
                self.result_text.insert(END, output + "\n\n")
                self.result_text.see(END)
                self.result_text.configure(state=DISABLED)
            
            self.root.after(0, update_ui)
        except Exception as e:
            self.root.after(0, lambda: self.handle_error(str(e)))

    def handle_error(self, err):
        self.progress.stop()
        self.scan_btn.config(state=NORMAL, text="START DEEP SCAN")
        messagebox.showerror("Scan Error", err)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScamCheckApp(root)
    root.mainloop()