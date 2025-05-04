"""
AI-to-SVG Video Generator with Full Agent Integration
This script converts AI prompts into SVG animations, processes them into PNG frames, and compiles them into a video.
It integrates intelligent agents from `agents.json` for dynamic prompt enhancement, color assignment, and motion design.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor

# ===== Constants =====
DEFAULT_CONFIG_PATH = "ai_svg_prompts.json"
AGENTS_CONFIG_PATH = "agents.json"
OUTPUT_DIR = Path("svg_frames")
LOG_FILE = "pipeline.log"

# ===== Logging Setup =====
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===== Utility Functions =====

def load_json_file(file_path: str) -> Dict:
    """
    Loads a JSON file and returns its content.
    Raises meaningful errors if the file is missing or malformed.
    """
    if not Path(file_path).exists():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        raise ValueError(f"Invalid JSON format in {file_path}: {e}")


def validate_config(config: Dict, required_fields: List[str]):
    """
    Ensures the configuration contains all necessary fields.
    Logs and raises errors if any required fields are missing.
    """
    for field in required_fields:
        if field not in config:
            logging.error(f"Missing required field: {field}")
            raise ValueError(f"Configuration missing required field: {field}")


def execute_agent(agent: Dict, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes an agent's logic based on its configuration and given inputs.
    Simulates agent execution by returning mock outputs for the pipeline.
    """
    logging.info(f"Executing agent: {agent['name']}")
    outputs = {}

    # Mock logic for each agent
    if agent["name"] == "SceneInspireAgent":
        outputs["inspired_prompt"] = f"{inputs['raw_prompt']} (Enhanced with metaphors)"
    elif agent["name"] == "ColorAuraAgent":
        emotion = "hope"  # Example emotion (determine dynamically in real implementation)
        outputs["background_color"] = agent["logic"]["color_mapping"].get(emotion, "#ffffff")
        outputs["accent_color"] = "#000000"  # Example default accent color
        outputs["mood_profile"] = emotion
    elif agent["name"] == "MotionMoodAgent":
        emotion_tone = inputs.get("emotion_tone", "awe")
        outputs["animation_style"] = agent["logic"]["emotion_mapped_motion"].get(emotion_tone, "default")
        outputs["pulse_rate"] = 1.5  # Example default pulse rate
        outputs["motion_curve"] = "sine-wave"
    else:
        logging.warning(f"Unknown agent: {agent['name']}")
    return outputs


def save_svg(svg_data: str, index: int) -> Path:
    """
    Saves SVG data to a file within the output directory.
    Ensures the directory exists before saving.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = OUTPUT_DIR / f"frame_{index:03d}.svg"
    file_path.write_text(svg_data)
    logging.info(f"SVG frame saved: {file_path}")
    return file_path


def convert_svg_to_png(svg_file: Path, width: int, height: int) -> Path:
    """
    Converts an SVG file to a PNG using Inkscape.
    Logs and raises errors if the conversion fails.
    """
    png_file = svg_file.with_suffix(".png")
    command = f"inkscape {svg_file} --export-filename={png_file} --export-width={width} --export-height={height}"
    if os.system(command) != 0:
        logging.error(f"Inkscape conversion failed for {svg_file}")
        raise RuntimeError(f"Inkscape conversion failed for {svg_file}")
    logging.info(f"PNG generated: {png_file}")
    return png_file


def create_video_from_pngs(output_file: str, frame_rate: int):
    """
    Compiles PNG frames into a video using FFMPEG.
    Logs and raises errors if the video creation fails.
    """
    command = f"ffmpeg -y -framerate {frame_rate} -i {OUTPUT_DIR}/frame_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p {output_file}"
    if os.system(command) != 0:
        logging.error("FFMPEG failed to create video")
        raise RuntimeError("FFMPEG failed to create video")
    logging.info(f"Video created: {output_file}")


# ===== Main Pipeline =====

def run_pipeline(config_path: str = DEFAULT_CONFIG_PATH, agents_path: str = AGENTS_CONFIG_PATH):
    """
    Executes the SVG-to-Video pipeline with integrated agents.
    Follows a modular approach for prompt enhancement, SVG generation, and video compilation.
    """
    try:
        # Step 1: Load and validate configurations
        config = load_json_file(config_path)
        agents = load_json_file(agents_path)
        validate_config(config, ["prompts", "width", "height", "output_video"])

        prompts = config["prompts"]
        width = config["width"]
        height = config["height"]
        frame_rate = config.get("frame_rate", 1)
        output_video = config["output_video"]

        # Step 2: Initialize agents
        scene_agent = next((agent for agent in agents if agent["name"] == "SceneInspireAgent"), {})
        color_agent = next((agent for agent in agents if agent["name"] == "ColorAuraAgent"), {})
        motion_agent = next((agent for agent in agents if agent["name"] == "MotionMoodAgent"), {})

        # Step 3: Process prompts and generate SVG frames
        logging.info("Starting SVG generation...")
        svg_files = []
        for idx, prompt in enumerate(prompts):
            # Apply SceneInspireAgent for prompt enhancement
            enhanced_prompt = execute_agent(scene_agent, {"raw_prompt": prompt, "frame_index": idx}).get("inspired_prompt", prompt)

            # Apply ColorAuraAgent for color schemes
            colors = execute_agent(color_agent, {"prompt": enhanced_prompt, "frame_index": idx})
            background_color = colors.get("background_color", "#f0f2f5")
            accent_color = colors.get("accent_color", "#333")

            # Apply MotionMoodAgent for animation styles
            motion = execute_agent(motion_agent, {"enhanced_prompt": enhanced_prompt, "emotion_tone": colors.get("mood_profile", "neutral")})
            pulse_rate = motion.get("pulse_rate", 1.0)

            # Generate SVG frame
            svg_data = f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{background_color}"/>
  <text x="20" y="40" fill="{accent_color}">Scene {idx + 1}</text>
  <text x="20" y="80" fill="{accent_color}">{enhanced_prompt}</text>
  <circle cx="{width // 2}" cy="{height - 60}" r="20" fill="{accent_color}">
    <animate attributeName="r" values="20;30;20" dur="{pulse_rate}s" repeatCount="indefinite"/>
  </circle>
</svg>"""
            svg_file = save_svg(svg_data, idx)
            svg_files.append(svg_file)

        # Step 4: Convert SVGs to PNGs in parallel
        logging.info("Starting SVG-to-PNG conversion...")
        with ThreadPoolExecutor() as executor:
            executor.map(lambda svg: convert_svg_to_png(svg, width, height), svg_files)

        # Step 5: Compile PNGs into a video
        logging.info("Starting video compilation...")
        create_video_from_pngs(output_video, frame_rate)

        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()