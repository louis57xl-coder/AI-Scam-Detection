import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, END, NORMAL, DISABLED
from tkinter import ttk
import threading
import re
import traceback

# --- AUTOMATIC REPAIR ---
try:
    from google import genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "google-genai"])
    from google import genai

class ScamCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScamScanner Pro - Stable Version")
        self.root.geometry("1100x950") 

        # --- TOP API KEY SECTION ---
        api_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
        api_frame.pack(fill=tk.X)
        
        tk.Label(api_frame, text="Gemini API Key:", font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=(20, 10))
        
        self.api_entry = tk.Entry(api_frame, font=("Consolas", 10), width=50, show="*")
        self.api_entry.pack(side=tk.LEFT, padx=5)
        
        # Right-click menu for API key
        self.api_menu = Menu(self.api_entry, tearoff=0)
        self.api_menu.add_command(label="Paste Key", command=lambda: self.safe_paste(self.api_entry))
        self.api_entry.bind("<Button-3>", lambda e: self.api_menu.post(e.x_root, e.y_root))

        self.apply_btn = tk.Button(api_frame, text="Apply Key", command=self.apply_key, bg="#4CAF50", fg="white", font=("Segoe UI", 9, "bold"))
        self.apply_btn.pack(side=tk.LEFT, padx=10)

        self.client = None

        # --- MAIN UI AREA ---
        main_container = tk.Frame(root, bg="white")
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(main_container, text="PASTE SUSPICIOUS TEXT BELOW:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor=tk.W, pady=(0, 10))
        
        self.input_text = scrolledtext.ScrolledText(main_container, height=12, font=("Segoe UI", 11), bd=2, highlightthickness=1)
        self.input_text.pack(fill=tk.BOTH, pady=5)

        # Right-click menu for Main Input box
        self.input_menu = Menu(self.input_text, tearoff=0)
        self.input_menu.add_command(label="Paste Text", command=lambda: self.safe_paste(self.input_text))
        self.input_text.bind("<Button-3>", lambda e: self.input_menu.post(e.x_root, e.y_root))

        self.scan_btn = tk.Button(main_container, text="START DEEP SCAN", font=("Segoe UI", 14, "bold"), bg="#1A73E8", fg="white", height=2, command=self.start_scan, state=DISABLED)
        self.scan_btn.pack(fill=tk.X, pady=20)

        self.progress = ttk.Progressbar(main_container, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))

        tk.Label(main_container, text="DETAILED SCAN RESULTS:", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor=tk.W)
        self.result_text = scrolledtext.ScrolledText(main_container, height=18, font=("Segoe UI", 10), bg="#f9f9f9", state=DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.result_text.tag_config("high", foreground="red", font=("Segoe UI", 12, "bold"))
        self.result_text.tag_config("med", foreground="orange", font=("Segoe UI", 12, "bold"))

    def safe_paste(self, widget):
        """Standardizes pasting across all platforms."""
        try:
            clipboard = self.root.clipboard_get()
            if isinstance(widget, tk.Entry):
                widget.delete(0, END) # Clear current content if pasting a key
                widget.insert(END, clipboard)
            else:
                widget.insert(tk.INSERT, clipboard)
        except:
            pass # Handle empty clipboard gracefully

    def apply_key(self):
        key = self.api_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Please enter a valid API key.")
            return
        try:
            self.client = genai.Client(api_key=key)
            self.scan_btn.config(state=NORMAL)
            messagebox.showinfo("Success", "API Key Applied!")
        except Exception as e:
            messagebox.showerror("Key Error", f"Could not initialize: {e}")

    def start_scan(self):
        text = self.input_text.get("1.0", END).strip()
        if not text:
            messagebox.showwarning("Empty", "Please paste text to analyze.")
            return
        self.scan_btn.config(state=DISABLED, text="SCANNING...")
        self.progress.start()
        threading.Thread(target=self.run_analysis, args=(text,), daemon=True).start()

    def run_analysis(self, text):
        try:
            prompt = f"Analyze for scams. Provide score 0-100 and reasoning.\nTEXT: {text}"
            response = self.client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
            output = response.text.strip()
            
            score = 0
            match = re.search(r"(\d+)", output)
            if match: score = int(match.group(1))
            
            def update_ui():
                self.progress.stop()
                self.scan_btn.config(state=NORMAL, text="START DEEP SCAN")
                self.result_text.configure(state=NORMAL)
                self.result_text.delete("1.0", END)
                self.result_text.insert(END, f"SCAM RISK RATING: {score}%\n", "high" if score >= 70 else "med")
                self.result_text.insert(END, output)
                self.result_text.configure(state=DISABLED)
            
            self.root.after(0, update_ui)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ScamCheckApp(root)
        root.mainloop()
    except Exception:
        # If the app crashes on launch, this keeps the error visible
        import tkinter.messagebox
        error_info = traceback.format_exc()
        # Create a tiny hidden root just to show the error
        temp_root = tk.Tk()
        temp_root.withdraw()
        tkinter.messagebox.showerror("Startup Crash", error_info)