from PIL import Image
from PIL.ImageSequence import Iterator
import streamlit as st, os, tempfile

FILE_ADD_NAME = '_trimmed'

def trim_gif_ui(path):
    gif = Image.open(path)
    st.write("Trim your gif (max 100% per value to the middle)")
    right = st.slider("Right crop %", min_value=0, max_value=int(100), value=0, step=5)
    left = st.slider("Left crop %", min_value=0, max_value=int(100), value=0, step=5)
    top = st.slider("Top crop %", min_value=0, max_value=int(100), value=0, step=5)
    bottom = st.slider("Bottom crop %", min_value=0, max_value=int(100), value=0, step=5)

    st.write(f"Right: {right}, Left: {left}, Top: {top}, Bottom: {bottom}")

    if st.button("Crop"):
        crop_area = (
            int(gif.width / 100 * left / 2),
            int(gif.height / 100 * top / 2),
            int(gif.width - gif.width / 100 * right / 2),
            int(gif.height - gif.height / 100 * bottom / 2),
        )
        frames = [frame.crop(crop_area) for frame in Iterator(gif)]
        
        
        base = os.path.basename(path)
        base = os.path.splitext(base)[0] + FILE_ADD_NAME + '.gif'
        
        path_to_gif = os.path.join("temp", base)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
            temp_gif_path = tmp_file.name
        
        
        frames[0].save(
            temp_gif_path,
            save_all=True,
            append_images=frames[1:],
            loop=gif.info.get("loop", 0),
            duration=gif.info.get("duration", 100),
            disposal=gif.info.get("disposal", 2)
        )

        os.replace(temp_gif_path, path_to_gif)
        st.success("Added caption to .gif!")
        st.rerun()
        
        return True