# 🎭 GIF Tool Local

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview
GIF Tool Local is a Python-powered tool that converts images and videos into GIFs and allows users to add captions and manage GIF history via a Streamlit web UI.

## ✨ Features
- Convert images and videos (PNG, JPG, JPEG, MP4, MOV, WEBM) to GIF
- Preview images and videos before conversion
- Adjust conversion speed and skip frames for videos
- Add multi-line captions to GIFs
- Manage active GIFs and GIF history through the UI

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

## ❗ Troubleshooting
Common issues and solutions:

1. **FFMPEG not found**
   - Ensure FFMPEG is properly installed
   - Try reinstalling the imageio[ffmpeg] package

2. **Memory Issues**
   - Reduce input video length
   - Increase frame skip rate
   - Lower the output resolution

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