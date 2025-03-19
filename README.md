# GIF Tool Local

## Overview
GIF Tool Local is a Python-powered tool that converts images and videos into GIFs and allows users to add captions and manage GIF history via a Streamlit web UI.

## Features
- Convert images and videos (PNG, JPG, JPEG, MP4, MOV, WEBM) to GIF
- Adjust conversion speed and skip frames for videos
- Add multi-line captions to GIFs
- Manage active GIFs and GIF history through the UI

## Requirements
- Python 3.x
- Dependencies listed in [requirements.txt](requirements.txt):
  - imageio[ffmpeg]
  - streamlit
  - pillow

## Setup Instructions
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

## Project Structure
- **main.py**: Main Streamlit application.
- **modules/**
  - `to_gif_tools.py`: Contains video and image to GIF conversion logic.
  - `caption_gif.py`: Adds configurable captions to GIFs.
  - `gif_class.py`: Defines the GifHolder class for GIF metadata.
- **requirements.txt**: Lists required Python packages.
- **.gitignore**: Specifies files and directories excluded from version control.
- **.streamlit/config.toml**: Streamlit server configuration.

## Usage
1. Launch the application and upload an image or video.
2. Set the desired speed and frame skip parameters.
3. Convert the file to a GIF.
4. (Optional) Use the caption tool to add text overlays on GIFs.
5. Manage, view, and download your active GIF or GIF history via the UI.

## Additional Notes
- The tool resizes GIFs to a fixed width for captioning while preserving aspect ratio.
- Temporary files and resized GIFs are stored in the `temp` folder.
- Font assets for captioning should reside in `modules/assets/fonts/`.