import to_gif_tools as gt
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
        if st.button("Convert to GIF"):
            # Save the uploaded file temporarily
            temp_path = f"temp//temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Convert to GIF
            with st.spinner(text="Converting to .gif...", show_time=True):
                gt.convert_to_gif(temp_path)
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
    
    st.subheader("Tabs")
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    with tab1:
        st.write("Content for tab 1")
    with tab2:
        st.write("Content for tab 2")
    with tab3:
        st.write("Content for tab 3")