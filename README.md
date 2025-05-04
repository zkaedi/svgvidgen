# AI-to-SVG Video Generator 🎬✨

This project enables **automated video generation** from AI prompts using SVG animations. It includes:

- 🧠 Prompt-to-SVG generation pipeline
- 🎛️ GUI interface for config selection and execution
- 📄 JSON config format
- 🎞️ PNG to video rendering via FFMPEG
- 🧰 Fully modular and extensible architecture

---

## 📦 Contents

- `ai_to_svg_pipeline_refined.py`: Main logic for prompt-to-SVG video generation
- `ai_to_svg_gui_refined.py`: GUI launcher using tkinter
- `ai_svg_prompts.json`: Sample JSON prompt file
- `ai_to_svg_mastery_refined.html`: Full HTML mastery documentation

---

## 🚀 Quickstart

1. **Install Dependencies**

```bash
pip install -r requirements.txt
sudo apt install ffmpeg inkscape  # Or brew install on macOS
```

2. **Run the GUI**

```bash
python ai_to_svg_gui_refined.py
```

3. **Or run pipeline directly**

```bash
python ai_to_svg_pipeline_refined.py ai_svg_prompts.json
```

---

## 🧠 JSON Config Example

```json
{
  "title": "AI SVG Video Prompt Set",
  "frame_rate": 1,
  "width": 400,
  "height": 200,
  "output_video": "ai_svg_video.mp4",
  "prompts": [
    "Scene 1: Opening shimmer",
    "Scene 2: Circle transforms into data node",
    "Scene 3: Light pulses outward"
  ]
}
```

---

## 🛠 Troubleshooting

- **FFMPEG not found**: Ensure it's in your PATH.
- **Inkscape issues**: Requires CLI-compatible version (`--export-png` support).
- **Permission errors**: Try running with `sudo` or check write access.

---

## 🌐 Project Goals

This project is designed for:
- Educators and visual storytellers
- AI prompt engineers
- SVG animation developers
- Creative coders and tinkerers

---

## 📜 License

MIT License – Free for commercial and non-commercial use.

