# 🎭 GIF Tool Local

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-FF4B4B.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

<img src="https://media.giphy.com/media/3oKIPEqDGUULpEU0aQ/giphy.gif" width="400" alt="Demo GIF">

**🚀 A powerful local GIF manipulation tool with a modern web interface**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tips](#-tips--tricks) • [Troubleshooting](#-troubleshooting)

</div>

## 🎯 Overview
GIF Tool Local is a Python-powered tool that transforms your media into GIFs with powerful editing capabilities. Built with Streamlit, it offers an intuitive interface for converting, editing, and managing your GIF collection.

## ✨ Features

<table>
<tr>
<td width="50%">

### Core Features
- 🎥 Convert various media to GIF
- 🖼️ Smart image processing
- 📝 Multi-line captions
- 🕹️ Interactive controls
- 📦 History management

</td>
<td width="50%">

### Supported Formats
- 📸 Images: `PNG, JPG, JPEG`
- 🎬 Videos: `MP4, MOV, WEBM`
- 🎭 Existing GIFs

</td>
</tr>
</table>

## 🔧 Requirements
- Python 3.x
- Dependencies listed in [requirements.txt](requirements.txt):
  - imageio[ffmpeg]
  - streamlit
  - pillow
  - opencv-python
  - numpy
  - ffmpeg-python

## 🚀 Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure the following directories exist (tracked via .gitkeep files):
   - output
   - temp
   - history
3. Run the web app:
   - Via the provided batch file:
     ```bat
     run.bat
     ```
   - Or directly with:
     ```bash
     python -m streamlit run main.py
     ```

## 🎨 Tools & Capabilities

### 1️⃣ Conversion Tools
- **Speed Control**: `0.1x` to `20.0x`
- **Frame Selection**: Skip frames to optimize size
- **Smart Resizing**: Maintains aspect ratio

### 2️⃣ Edit Tools
- **Crop Tool**: Precise visual cropping
- **Caption Tool**: Multi-line text with custom fonts
- **Optimize Tool**: Reduce file size while maintaining quality

### 3️⃣ Management
- **History System**: Keep track of all operations
- **Active GIF**: Work on one GIF at a time
- **Quick Export**: Download processed GIFs instantly

## 📁 Project Structure
- **main.py**: Main Streamlit application.
- **modules/**
  - `to_gif_tools.py`: Contains video and image to GIF conversion logic.
  - `caption_gif.py`: Adds configurable captions to GIFs.
  - `gif_class.py`: Defines the GifHolder class for GIF metadata.
- **requirements.txt**: Lists required Python packages.
- **.gitignore**: Specifies files and directories excluded from version control.
- **.streamlit/config.toml**: Streamlit server configuration.

## 📝 Usage

<details>
<summary>🎬 Converting Media to GIF</summary>

1. Upload your media file
2. Adjust conversion parameters:
   - `Speed`: Controls playback speed
   - `Frame Skip`: Reduces file size
3. Click "Convert/upload GIF"

</details>

<details>
<summary>✏️ Adding Captions</summary>

1. Select a GIF from history
2. Navigate to "Caption .gif" tab
3. Enter your text
4. Click "Add caption"

</details>

1. Launch the application and upload an image or video.
2. Preview your media file to ensure correct orientation and content.
3. Set the desired speed and frame skip parameters.
4. Convert the file to a GIF.
5. (Optional) Use the caption tool to add text overlays on GIFs.
6. Manage, view, and download your active GIF or GIF history via the UI.

## 💡 Tips & Tricks
- Use lower frame rates (10-15 fps) for smoother, smaller GIFs
- Optimal GIF width is typically between 400-800 pixels
- Consider file size vs. quality tradeoffs when adjusting parameters
- Use short, punchy captions for better readability

## 🔍 Advanced Features

### Performance Optimization
```python
# Recommended settings for optimal output
Speed: 1.0          # Standard playback
Frame Skip: 4       # Good balance
Resolution: 400px   # Standard width
Colors: 256         # Maximum quality
```

### File Size Guide
| Quality Level | Colors | Typical Size |
|--------------|--------|--------------|
| Maximum      | 256    | Original     |
| High         | 128    | ~70%        |
| Medium       | 64     | ~50%        |
| Low          | 32     | ~30%        |

## ❗ Troubleshooting
Common issues and solutions:

1. **FFMPEG not found**
   - Ensure FFMPEG is properly installed
   - Try reinstalling the imageio[ffmpeg] package

2. **Memory Issues**
   - Reduce input video length
   - Increase frame skip rate
   - Lower the output resolution

## 🌟 Pro Tips
> 💡 Use frame skip of 4 for smooth animations while reducing file size
> 
> 🎨 Keep captions under 2 lines for best visibility
> 
> 📊 Start with high quality, then optimize if needed

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📋 Additional Notes
- The tool resizes GIFs to a fixed width for captioning while preserving aspect ratio.
- Temporary files and resized GIFs are stored in the `temp` folder.
- Font assets for captioning should reside in `modules/assets/fonts/`.