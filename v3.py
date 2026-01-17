import sys
import subprocess

# --- AUTOMATIC REPAIR ---
try:
    from google import genai
    from google.genai import types
except (ImportError, NameError):
    print("Repairing library: google-genai...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "google-genai"])
    from google import genai
    from google.genai import types

import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, END, NORMAL, DISABLED
import threading
import re

# YOUR ACTUAL KEY
MY_API_KEY = "AIzaSyDjZVNwgBzp-qBeKo1sMDRSlkzozegnOBA"

class ScamCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScamCheck - Gemini 2.5 Flash-Lite")
        self.root.geometry("1100x950") 

        # Initialize Client
        try:
            self.client = genai.Client(api_key=MY_API_KEY)
        except Exception as e:
            print(f"Connection Error: {e}")

        # --- UI ELEMENTS ---
        tk.Label(root, text="Analysis Results", font=("Segoe UI", 12, "bold")).pack(pady=5, padx=20, anchor="w")
        
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, font=("Consolas", 11), state=DISABLED)
        self.result_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Tags for color coding
        self.result_text.tag_config("high", foreground="red", font=("Consolas", 18, "bold"))
        self.result_text.tag_config("med", foreground="orange", font=("Consolas", 18, "bold"))
        self.result_text.tag_config("low", foreground="green", font=("Consolas", 18, "bold"))

        tk.Label(root, text="Paste message here (Right-Click enabled):", font=("Segoe UI", 11, "bold")).pack(pady=5, padx=20, anchor="w")
        
        self.input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, font=("Consolas", 11), undo=True)
        self.input_text.pack(padx=20, pady=5, fill=tk.BOTH)

        # ─── RIGHT-CLICK MENU SETUP ───
        self.menu = Menu(root, tearoff=0)
        self.menu.add_command(label="Cut", command=lambda: self.input_text.event_generate("<<Cut>>"))
        self.menu.add_command(label="Copy", command=lambda: self.input_text.event_generate("<<Copy>>"))
        self.menu.add_command(label="Paste", command=lambda: self.input_text.event_generate("<<Paste>>"))
        self.menu.add_separator()
        self.menu.add_command(label="Select All", command=lambda: self.input_text.tag_add("sel", "1.0", END))

        # Bind right-click to the input box
        self.input_text.bind("<Button-3>", self.show_context_menu)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Gemini Deep Scan", command=self.start_scan, bg="#4CAF50", fg="white", width=20, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear All", command=self.clear, width=12).pack(side=tk.LEFT, padx=10)

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def clear(self):
        self.input_text.delete("1.0", END)
        self.result_text.configure(state=NORMAL)
        self.result_text.delete("1.0", END)
        self.result_text.configure(state=DISABLED)

    def start_scan(self):
        msg = self.input_text.get("1.0", END).strip()
        if not msg: return
        self.result_text.configure(state=NORMAL)
        self.result_text.insert(END, "\n" + "="*80 + "\nANALYZING WITH GEMINI 2.5 FLASH-LITE...\n" + "="*80 + "\n")
        self.result_text.configure(state=DISABLED)
        threading.Thread(target=self.do_gemini, args=(msg,), daemon=True).start()

    def do_gemini(self, text):
        try:
            # High-pressure prompt for strict rating
            prompt = f"""Analyze this for pig-butchering and romance scams. 
            Start your reply with 'SCAM SCORE: X/100'. 
            Be blunt about the risk level.
            
            Text to analyze: {text}"""
            
            response = self.client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
            output = response.text.strip()
            
            # Score parsing logic
            score = 0
            match = re.search(r"SCORE:\s*(\d+)", output, re.IGNORECASE)
            if match: score = int(match.group(1))

            tag = "low"
            if score >= 80: tag = "high"
            elif score >= 40: tag = "med"

            def update_ui():
                self.result_text.configure(state=NORMAL)
                self.result_text.insert(END, f"SCAM PROBABILITY RATING: {score}%\n", tag)
                self.result_text.insert(END, output + "\n" + "-"*80 + "\n")
                self.result_text.see(END)
                self.result_text.configure(state=DISABLED)

            self.root.after(0, update_ui)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("API Error", str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = ScamCheckApp(root)
    root.mainloop()