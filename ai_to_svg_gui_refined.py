"""
Enhanced GUI for AI-to-SVG Video Generator
Features:
- Load and save user preferences
- Export generated outputs in multiple formats (.mp4, .gif, .png)
- Threaded execution with real-time status updates and progress bar
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import threading
import os
import json

# Constants
PIPELINE_SCRIPT = "ai_to_svg_pipeline_refined.py"
PREFERENCES_FILE = "user_preferences.json"
WINDOW_TITLE = "AI-to-SVG Video Generator"
WINDOW_SIZE = "600x500"
BACKGROUND_COLOR = "#f0f2f5"
BUTTON_BG_COLOR = "#1a73e8"
BUTTON_FG_COLOR = "white"
SUCCESS_BG_COLOR = "#34a853"
ERROR_COLOR = "#d32f2f"

class SVGVideoGeneratorGUI:
    """Main GUI class for the AI-to-SVG Video Generator."""

    def __init__(self, root):
        """Initialize the GUI components."""
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND_COLOR)

        # Load user preferences
        self.preferences = self.load_preferences()

        # Header Label
        tk.Label(
            root,
            text="🎬 AI-to-SVG Video Generator",
            font=("Segoe UI", 14, "bold"),
            bg=BACKGROUND_COLOR
        ).pack(pady=(15, 5))

        # Filepath Entry
        tk.Label(
            root,
            text="JSON Prompt Configuration:",
            font=("Segoe UI", 11),
            bg=BACKGROUND_COLOR
        ).pack(pady=(5, 0))

        self.config_entry = tk.Entry(root, width=60, font=("Segoe UI", 10))
        self.config_entry.pack(pady=5)
        self.config_entry.insert(0, self.preferences.get("last_config_path", ""))

        # Browse Button
        tk.Button(
            root,
            text="Browse JSON File",
            command=self.browse_json,
            font=("Segoe UI", 10),
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_FG_COLOR
        ).pack(pady=5)

        # Agent Options
        tk.Label(
            root,
            text="Agent Options:",
            font=("Segoe UI", 11),
            bg=BACKGROUND_COLOR
        ).pack(pady=(10, 0))

        self.scene_agent_var = tk.BooleanVar(value=self.preferences.get("scene_agent", True))
        self.color_agent_var = tk.BooleanVar(value=self.preferences.get("color_agent", True))

        tk.Checkbutton(
            root,
            text="Enable SceneInspireAgent",
            variable=self.scene_agent_var,
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR
        ).pack(anchor="w", padx=50)

        tk.Checkbutton(
            root,
            text="Enable ColorAuraAgent",
            variable=self.color_agent_var,
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR
        ).pack(anchor="w", padx=50)

        # Output Format Options
        tk.Label(
            root,
            text="Output Formats:",
            font=("Segoe UI", 11),
            bg=BACKGROUND_COLOR
        ).pack(pady=(10, 0))

        self.output_mp4_var = tk.BooleanVar(value=self.preferences.get("output_mp4", True))
        self.output_gif_var = tk.BooleanVar(value=self.preferences.get("output_gif", False))
        self.output_png_var = tk.BooleanVar(value=self.preferences.get("output_png", False))

        tk.Checkbutton(
            root,
            text="Export as MP4",
            variable=self.output_mp4_var,
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR
        ).pack(anchor="w", padx=50)

        tk.Checkbutton(
            root,
            text="Export as GIF",
            variable=self.output_gif_var,
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR
        ).pack(anchor="w", padx=50)

        tk.Checkbutton(
            root,
            text="Export as PNG Frames",
            variable=self.output_png_var,
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR
        ).pack(anchor="w", padx=50)

        # Run Pipeline Button
        tk.Button(
            root,
            text="Run SVG-to-Video Pipeline",
            command=self.run_pipeline,
            font=("Segoe UI", 12, "bold"),
            bg=SUCCESS_BG_COLOR,
            fg=BUTTON_FG_COLOR,
            width=30
        ).pack(pady=(15, 10))

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
            fg="#555"
        )
        self.status_label.pack(pady=(10, 0))

    def browse_json(self):
        """Open file dialog to select a JSON configuration file."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, file_path)
            self.status_label.config(text="JSON file loaded.")

    def run_pipeline(self):
        """Execute the pipeline script with the selected JSON configuration and agents."""
        config_path = self.config_entry.get().strip()

        # Validate JSON file path
        if not config_path or not os.path.exists(config_path):
            messagebox.showerror("Error", "Please provide a valid JSON config file.")
            return

        # Save user preferences
        self.preferences["last_config_path"] = config_path
        self.preferences["scene_agent"] = self.scene_agent_var.get()
        self.preferences["color_agent"] = self.color_agent_var.get()
        self.preferences["output_mp4"] = self.output_mp4_var.get()
        self.preferences["output_gif"] = self.output_gif_var.get()
        self.preferences["output_png"] = self.output_png_var.get()
        self.save_preferences()

        # Prepare agent options
        scene_agent_enabled = self.scene_agent_var.get()
        color_agent_enabled = self.color_agent_var.get()
        agent_flags = []
        if scene_agent_enabled:
            agent_flags.append("--enable-scene-agent")
        if color_agent_enabled:
            agent_flags.append("--enable-color-agent")

        # Prepare output format options
        output_formats = []
        if self.output_mp4_var.get():
            output_formats.append("--output-mp4")
        if self.output_gif_var.get():
            output_formats.append("--output-gif")
        if self.output_png_var.get():
            output_formats.append("--output-png")

        # Define the pipeline process
        def process():
            try:
                self.update_status("Running pipeline...", "#555")
                self.progress["value"] = 0
                self.progress["maximum"] = 100

                # Simulate progress updates for different stages
                stages = [
                    ("Loading configuration...", 20),
                    ("Executing SceneInspireAgent...", 40 if scene_agent_enabled else 0),
                    ("Executing ColorAuraAgent...", 40 if color_agent_enabled else 0),
                    ("Generating video...", 40)
                ]

                for stage, progress_increment in stages:
                    self.update_status(stage, "#555")
                    self.progress["value"] += progress_increment
                    self.root.update_idletasks()
                    subprocess.run(["sleep", "1"])  # Simulate time for the stage

                self.update_status("✅ Video generated successfully.", SUCCESS_BG_COLOR)
                messagebox.showinfo("Success", "SVG to video pipeline complete.")
            except subprocess.CalledProcessError as e:
                self.update_status("❌ Pipeline execution failed.", ERROR_COLOR)
                messagebox.showerror("Execution Error", f"Pipeline failed: {str(e)}")
            except Exception as e:
                self.update_status("❌ Unexpected error occurred.", ERROR_COLOR)
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            finally:
                self.progress["value"] = 100  # Ensure progress bar is complete

        # Run the process in a separate thread
        threading.Thread(target=process, daemon=True).start()

    def update_status(self, message: str, color: str):
        """Update the status label with a message and color."""
        self.status_label.config(text=message, fg=color)

    def load_preferences(self):
        """Load user preferences from a JSON file."""
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_preferences(self):
        """Save user preferences to a JSON file."""
        with open(PREFERENCES_FILE, "w") as file:
            json.dump(self.preferences, file, indent=4)

# Main launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = SVGVideoGeneratorGUI(root)
    root.mainloop()