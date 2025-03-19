from PIL import Image
import streamlit as st
import os, base64, shutil

import modules.to_gif_tools as gt
import modules.gif_class as gc




def move_gif_active(gif_path):
    gt.__delete_output__()

    filename = os.path.basename(gif_path)
    destination_file_path = os.path.join(r"output", "output.gif")

    shutil.copy2(gif_path, destination_file_path)
    print(f"Moved {filename} to output directory")




if 'active_gif_cached' not in st.session_state:
    st.session_state['active_gif_cached'] = None

active_gif = None

if st.session_state['active_gif_cached'] is not None:
    active_gif = gc.GifHolder(st.session_state['active_gif_cached'])
    move_gif_active(active_gif.path)

gif_history = []


a = os.listdir("history")
for file in a:
    if file.endswith(".gitkeep"):
        continue

    gif_history.append(file)

def new_gif():
    files = os.listdir("temp")

    path_to_gif = None

    for file in files:
        if file[-4:] == ".gif":
            path_to_gif = os.path.join("temp", file)
            break

    if path_to_gif is None:
        print("No .gif found in temp directory")
        return

    filename = os.path.basename(path_to_gif)
    destination_file_path = os.path.join(r"history", file)

    shutil.copy2(path_to_gif, destination_file_path)
    print(f"Moved {filename} to history directory")
        
    st.session_state['active_gif_cached'] = destination_file_path
    active_gif = gc.GifHolder(st.session_state['active_gif_cached'])

    move_gif_active(active_gif.path)



if __name__ == "__main__":
    # Clear temp folder at startup
    for file in os.listdir("temp"):
        if file != ".gitkeep":
            os.remove(os.path.join("temp", file))

    st.title("GIF Converter")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'webm'])

    if uploaded_file is not None:
        col1, col2, col3 = st.columns(3)

        with col2:
            speed_input = st.number_input("Speed (float)", min_value=0.1, max_value=6.0, value=1.0, step=0.5)

        with col3:
            skip_frame_input = st.number_input("Keep every frame (int)", min_value=0, max_value=20, value=4, step=0)

        with col1:
            if st.button("Convert to GIF"):
                # Save the uploaded file temporarily
                temp_path = f"temp/{uploaded_file.name}"

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Convert to GIF
                with st.spinner("Converting to .gif..."):
                    gt.convert_to_gif(temp_path, speed_input, skip_frame_input)

                uploaded_file.close()
                
                st.success(f"Converted {uploaded_file.name} to GIF!")
                new_gif()

    # Display the output GIF if it exists
    try:
        if os.path.exists(r"output/output.gif"):
            gif_image = open(r"output/output.gif", "rb")
            contents = gif_image.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            gif_image.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" style="max-height: 400px; display: block; margin-left: auto; margin-right: auto;">',
                unsafe_allow_html=True,
            )
        else:
            st.info("No active .gif found.")

    except Exception as e:
        st.error(f"Error loading GIF: {e}")
    
    st.subheader("")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        b = st.selectbox("Set gif active, from history", gif_history)
        if st.button("Set active"):
            st.session_state['active_gif_cached'] = os.path.join("history", b)
            active_gif = gc.GifHolder(st.session_state['active_gif_cached'])

            move_gif_active(active_gif.path)
            st.rerun()
        if st.button("Clear history"):
            for file in gif_history:
                if file != ".gitkeep":
                    os.remove(os.path.join("history", file))
                
            st.session_state['active_gif_cached'] = None
            active_gif = None
            st.rerun()


    with col2:
        if st.button("Remove active .gif"):
            if os.path.exists(r"output/output.gif"):
                os.remove(r"output/output.gif")
                st.session_state['active_gif_cached'] = None
                active_gif = None

                st.rerun()

    
    with col3:
        if os.path.exists(r"output/output.gif"):
            with open(r"output/output.gif", "rb") as f:
                gif_data = f.read()
                
            st.download_button(
                label="Click to download",
                data=gif_data,
                file_name="output.gif",
                mime="image/gif"
            )

        else:
            st.warning("No active .gif to download.")
    
    st.subheader("Tools")
    tab1, tab2, tab3 = st.tabs(["Crop", "Tab 2", "Tab 3"])
    with tab1:
        st.write("Content for tab 1")

    with tab2:
        st.write("Content for tab 2")

    with tab3:
        st.write("Content for tab 3")