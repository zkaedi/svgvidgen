"""
Refined AI-to-SVG Video Generator with Modular Design
Pure logic approach using JSON input, SVG generation, image conversion, and video compilation.
"""

import os
import json
import time
from pathlib import Path
from typing import List

# ===== Constants and Defaults =====
DEFAULT_CONFIG_PATH = "ai_svg_prompts.json"
OUTPUT_DIR = Path("svg_frames")

# ===== Utility Functions =====

def load_json_config(path: str) -> dict:
    if not Path(path).exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def generate_svg_frame(prompt: str, index: int, width: int, height: int) -> str:
    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    text {{ font-family: Arial; font-size: 20px; fill: #1a73e8; }}
    circle {{ fill: #ff4081; animation: pulse 1.5s infinite alternate; }}
    @keyframes pulse {{
      from {{ r: 20; }}
      to {{ r: 30; }}
    }}
  </style>
  <rect width="100%" height="100%" fill="#f0f2f5"/>
  <text x="20" y="40">Scene {index + 1}</text>
  <text x="20" y="80">{prompt}</text>
  <circle cx="{width // 2}" cy="{height - 60}" r="20"/>
</svg>"""

def save_svg(svg_data: str, index: int) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = OUTPUT_DIR / f"frame_{index:03d}.svg"
    file_path.write_text(svg_data)
    print(f"[SVG] Saved frame {index}: {file_path}")
    return file_path

def convert_svg_to_png(svg_file: Path, width: int, height: int) -> Path:
    png_file = svg_file.with_suffix(".png")
    command = f"inkscape {svg_file} --export-png={png_file} --export-width={width} --export-height={height}"
    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Inkscape conversion failed for {svg_file}")
    print(f"[PNG] Generated: {png_file}")
    return png_file

def create_video_from_pngs(output_file: str, frame_rate: int):
    command = f"ffmpeg -y -framerate {frame_rate} -i {OUTPUT_DIR}/frame_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p {output_file}"
    result = os.system(command)
    if result != 0:
        raise RuntimeError("FFMPEG failed to create video")
    print(f"[VIDEO] Output: {output_file}")

# ===== Main Logic =====

def run_pipeline(config_path: str = DEFAULT_CONFIG_PATH):
    config = load_json_config(config_path)
    prompts = config.get("prompts", [])
    width = config.get("width", 400)
    height = config.get("height", 200)
    frame_rate = config.get("frame_rate", 1)
    output_video = config.get("output_video", "ai_svg_video.mp4")

    # Step 1: Render SVGs
    for idx, prompt in enumerate(prompts):
        svg = generate_svg_frame(prompt, idx, width, height)
        save_svg(svg, idx)

    time.sleep(1)  # ensure all writes complete

    # Step 2: Convert to PNG
    for svg_path in sorted(OUTPUT_DIR.glob("*.svg")):
        convert_svg_to_png(svg_path, width, height)

    # Step 3: Compile into video
    create_video_from_pngs(output_video, frame_rate)

if __name__ == "__main__":
    run_pipeline()
