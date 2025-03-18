import modules.to_gif_tools as gt
from PIL import Image
import streamlit as st
import os, base64


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
                    # Remove temp file
                    os.remove(temp_path)
                    st.success(f"Converted {uploaded_file.name} to GIF!")


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

    if st.button("Remove active .gif"):
        if os.path.exists(r"output/output.gif"):
            os.remove(r"output/output.gif")

    if st.button("Download .gif"):
        if os.path.exists(r"output/output.gif"):
            with open(r"output/output.gif", "rb") as f:
                gif_data = f.read()
            st.download_button(
                label="Download .gif",
                data=gif_data,
                file_name="output.gif",
                mime="image/gif",
            )
        else:
            st.warning("No active .gif to download.")
    
    st.subheader("Tools")
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    with tab1:
        st.write("Content for tab 1")

    with tab2:
        st.write("Content for tab 2")

    with tab3:
        st.write("Content for tab 3")