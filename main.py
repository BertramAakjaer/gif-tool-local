import streamlit as st
import os, base64, shutil

import modules.to_gif_tools as gt
import modules.gif_class as gc
import modules.caption_gif as cg
import modules.trim_size_tool as tst
import modules.trim_gif_tool as tgt

#import modules.lossy_gif as lg

# Sætter en hovedet gif, til at arbejde på
def move_gif_active(gif_path):
    gt.__delete_output__()

    filename = os.path.basename(gif_path)
    destination_file_path = os.path.join(r"output", "output.gif")

    shutil.copy2(gif_path, destination_file_path)
    print(f"Moved {filename} to output directory")


# Sletter output filen, så der er klar til ny gif, ved startup
for file in os.listdir("output"):
    if file != ".gitkeep":
        os.remove(os.path.join("output", file))

active_gif = None

# Hvis der tidligere er blevet valgt en gif, så sætter den den som aktiv
if 'active_gif_cached' not in st.session_state:
    st.session_state['active_gif_cached'] = None
    
    if len(os.listdir("history")) > 1:
        temp = os.listdir("history")
        for file in temp:
            if file.endswith(".gif"):
                st.session_state['active_gif_cached'] = os.path.join("history", file)
                active_gif = gc.GifHolder(st.session_state['active_gif_cached'])
                move_gif_active(active_gif.path)
                break

# Opretter cache til den aktive gif, så den kan bruges i gemmem sessions
elif st.session_state['active_gif_cached'] is not None:
        active_gif = gc.GifHolder(st.session_state['active_gif_cached'])
        move_gif_active(active_gif.path)

# Funktion til at opdatere historikken af gifs, hente alle de tidligere gifs fra mappen
def update_history():
    gif_history = []


    a = os.listdir("history")
    for file in a:
        if file.endswith(".gitkeep"):
            continue

        gif_history.append(file)
    
    return gif_history

# Defineres her, så den kan bruges i main
gif_history = update_history()

# Når en ny gif laves, så flyttes den til temp mappen
# Denne funktion finder den nyeste gif i temp mappen og flytter den til history mappen
# og opdaterer den aktive gif

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
    
    # Rydder temp folder ved startup
    for file in os.listdir("temp"):
        if file != ".gitkeep":
            os.remove(os.path.join("temp", file))
    

    st.title("GIF Converter")

    # Fil uploader
    uploaded_file = st.file_uploader("Choose a file", type=['gif', 'png', 'jpg', 'jpeg', 'mp4', 'mov', 'webm'])

    # Hvis en fil er valgt, så vises der en knap til at konvertere den til gif
    if uploaded_file is not None:
        col1, col2, col3 = st.columns(3)

        with col2: # Vælg hastighed af gif
            speed_input = st.number_input("Speed (float)", min_value=0.1, max_value=20.0, value=1.0, step=0.5)

        with col3: # Vælg frames (til optimering af video til gif)
            skip_frame_input = st.number_input("Keep every frame (int)", min_value=0, max_value=60, value=4, step=0)

        with col1:
            if st.button("Convert/upload GIF"):
                temp_path = f"temp/{uploaded_file.name}"

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Convert to GIF
                with st.spinner("Converting to .gif..."):
                    gt.convert_to_gif(temp_path, speed_input, skip_frame_input)

                uploaded_file.close()
                
                st.success(f"Converted {uploaded_file.name} to GIF!")
                new_gif()
                gif_history = update_history()
                st.rerun()

    # Viser den aktive gif, hvis der er en, ved brug af markdown integration
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
            
            # Viser metadata om den aktive gif
            st.text(f"Name: {active_gif.name}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text(f"Widt: {active_gif.width} px")
                st.text(f"Height: {active_gif.height} px")
                
            with col2:
                st.text(f"Duration: {int(active_gif.clip_duration // 60)}m {int(active_gif.clip_duration % 60)}s ({active_gif.fps:.2f} fps)")
                st.text(f"Frames: {active_gif.frames}")
                
            with col3:
                st.text(f"Size: {active_gif.space:.2f} MB")
            
        else:
            st.info("No active .gif found.")

    except Exception as e:
        st.error(f"Error loading GIF: {e}")
    
    # Knapper til at slette den aktive gif og til at vælge en fra historikken
    if active_gif is not None:
        st.divider()
        
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
            try:
                if os.path.exists(active_gif.path):
                    with open(active_gif.path, "rb") as f:
                        gif_data = f.read()
                        
                    base = os.path.basename(active_gif.path)
                    base = os.path.splitext(base)[0] + '.gif'
                    
                    st.download_button(
                        label="Click to download",
                        data=gif_data,
                        file_name=base,
                        mime="image/gif"
                    )

                else:
                    st.warning("No active .gif to download.")
            except Exception as e:
                st.warning("No active .gif to download.")
        
    # Forskellige værktøjer til at arbejde med .gif'en
    if active_gif is not None:
        st.subheader("Tools")
        tab1, tab2, tab3, tab4 = st.tabs(["Crop", "Trim", "Caption .gif", "Optimize .gif"])
            
        with tab1: # Værktøj til at Croppe gif'en
            if os.path.exists(r"output/output.gif"):
                with st.spinner("Trimming GIF..."):
                    if tst.trim_gif_ui(active_gif.path):
                        st.success("Cropped to .gif!")
                        
                        new_gif()
                        st.rerun()
                        
            else:
                st.warning("No active .gif found.")

        with tab2: # Værktøj til at trimme gif'en
            st.title("Tool: Trim GIF")

            if os.path.exists(r"output/output.gif"):
                # Inputfælter til at brugeren sætter ind hvor meget der skal af
                col1, col2 = st.columns(2)
                with col1:
                    cut_start = st.number_input("Seconds to trim from start", min_value=0.0, max_value=30.0, value=0.0, step=0.1)
                with col2:
                    cut_end = st.number_input("Seconds to trim from end", min_value=0.0, max_value=30.0, value=2.0, step=0.1)

                if st.button("Trim GIF"):
                    try:
                        with st.spinner("Trimming GIF..."):
                            # Trimmer giffen og finder den folder den skal ende op i
                            tgt.trim_gif(active_gif.path, cut_start=cut_start, cut_end=cut_end)
                            new_gif()

                            st.success("GIF trimmed successfully.")
                            st.rerun()

                    # Giver en error message hvis der er fejl under trimming    
                    except Exception as e:
                        st.error(f"Failed to trim GIF: {e}")
            else:
                st.warning("No active .gif found.")

        with tab3: # Værktøj til at tilføje caption til gif'en
            st.title("Tool: Add caption to .gif")
            if os.path.exists(r"output/output.gif"):
                caption = st.text_input("Caption:")
                if st.button("Add caption"):
                    cg.add_caption_to_gif(active_gif.path, caption)
                    new_gif()
                    st.success("Added caption to .gif!")
                    st.rerun()
            else:
                st.warning("No active .gif found.")
        
        with tab4: # Værktøj til at optimere gif'en (ikke implementeret endnu)
            st.title("Tool: Optimize .gif")
