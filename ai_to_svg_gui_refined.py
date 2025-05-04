"""
Refined GUI for AI-to-SVG Video Generator
Features:
- Load JSON config file
- Launch refined pipeline script
- Threaded execution with real-time status
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os

PIPELINE_SCRIPT = "ai_to_svg_pipeline_refined.py"

class SVGVideoGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-to-SVG Video Generator")
        self.root.geometry("540x270")
        self.root.configure(bg="#f0f2f5")

        tk.Label(root, text="🎬 JSON Prompt Configuration", font=("Segoe UI", 13, "bold"), bg="#f0f2f5").pack(pady=(15, 5))

        self.config_entry = tk.Entry(root, width=60, font=("Segoe UI", 10))
        self.config_entry.pack(pady=5)

        tk.Button(root, text="Browse JSON File", command=self.browse_json,
                  font=("Segoe UI", 10), bg="#1a73e8", fg="white").pack(pady=5)

        tk.Button(root, text="Run SVG-to-Video Pipeline", command=self.run_pipeline,
                  font=("Segoe UI", 11, "bold"), bg="#34a853", fg="white", width=30).pack(pady=(10, 10))

        self.status_label = tk.Label(root, text="Ready", font=("Segoe UI", 9), bg="#f0f2f5", fg="#555")
        self.status_label.pack(pady=(10, 0))

    def browse_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, file_path)
            self.status_label.config(text="JSON file loaded.")

    def run_pipeline(self):
        config_path = self.config_entry.get().strip()
        if not config_path or not os.path.exists(config_path):
            messagebox.showerror("Error", "Please provide a valid JSON config file.")
            return

        def process():
            try:
                self.status_label.config(text="Running pipeline...")
                subprocess.run(["python3", PIPELINE_SCRIPT, config_path], check=True)
                self.status_label.config(text="✅ Video generated successfully.")
                messagebox.showinfo("Success", "SVG to video pipeline complete.")
            except subprocess.CalledProcessError as e:
                self.status_label.config(text="❌ Pipeline execution failed.")
                messagebox.showerror("Execution Error", str(e))

        threading.Thread(target=process).start()

# Main launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = SVGVideoGeneratorGUI(root)
    root.mainloop()
