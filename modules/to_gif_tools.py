import imageio, os, tempfile
from PIL import Image


def convert_to_gif(file_path, speed, skip_every_n_frames):
    __delete_output__()

    try:
        # Check if the file is a video
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
            __from_video__(file_path, skip_every_n_frames, speed)

        elif file_path.lower().endswith(('.jpeg', '.jpg', '.png', '.webp')):
            __from_image__(file_path)
        else:
            raise ValueError("Invalid file format.")
        
    except Exception as e:
        print(f"Error converting video: {str(e)}")




#######################################################################
#           HELPER FUNCTIONS TO RUN THE MAIN FUNCTIONS                #
#######################################################################



def __delete_output__():
    try:
        os.remove('output/output.gif')
        print("Deleted output.gif")
    except FileNotFoundError:
        print("output.gif not found")

def __from_video__(file_path, skip_every_n_frames, speed):
    abs_video_path = os.path.abspath(file_path.strip('"'))  # Remove any quotes from path
    
    # Read the video
    reader = imageio.get_reader(abs_video_path)
    meta_data = reader.get_meta_data()
    fps = meta_data['fps']
    print("Video metadata:", meta_data)  # This will show all available metadata
    
    # Get frames from video
    frames = []
    for i, frame in enumerate(reader):
        if i % skip_every_n_frames == 0:  # Only keep every fourth frame
            frames.append(frame)
    
    print(f"Read {len(frames)} frames from video")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
        temp_gif_path = tmp_file.name
    
    # Save as GIF in the temporary file
    imageio.mimsave(temp_gif_path, frames, fps=fps / (speed / skip_every_n_frames), loop=0)
    print(f"Saved GIF to {temp_gif_path}")
    
    # Move the temporary file to the output directory
    os.replace(temp_gif_path, r'output\output.gif')
    print("Moved GIF to output directory")
    
    print("Successfully created output.gif")

def __from_image__(file_path):
    try:
        img = Image.open(file_path)
        img.save('output/output.gif', save_all=True, append_images=[img], loop=0)
        print("Successfully created output.gif")
    except Exception as e:
        print(f"Error converting image: {str(e)}")


