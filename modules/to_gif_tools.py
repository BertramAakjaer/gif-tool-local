import imageio, os, tempfile, shutil
from PIL import Image


def convert_to_gif(file_path, speed, skip_every_n_frames): # Hovedet funktion, der finde filtypen og behandler den derefter
    __delete_output__()

    try:
        # Check if the file is a video
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
            __from_video__(file_path, skip_every_n_frames, speed) # Hvis det er en video

        elif file_path.lower().endswith(('.jpeg', '.jpg', '.png', '.webp')):
            __from_image__(file_path) # Hvis det er et billede
            
        elif file_path.lower().endswith('.gif'):
            __save_gif__(file_path) # Hvis det allerede er en gif (gemmes bare)
        else:
            raise ValueError("Invalid file format.")
        
    except Exception as e:
        print(f"Error converting video: {str(e)}")


def __delete_output__():
    try:
        os.remove('output/output.gif')
        print("Deleted output.gif")
    except FileNotFoundError:
        print("output.gif not found")


#######################################################################
#           HELPER FUNCTIONS TO RUN THE MAIN FUNCTIONS                #
#######################################################################



def __from_video__(file_path, skip_every_n_frames, speed):
    abs_video_path = os.path.abspath(file_path.strip('"'))  # Fjerner eventuelle citationstegn fra filstien (var vigtig tidligere i produktion, men skader ikke)
    
    # Læser videoen ind
    reader = imageio.get_reader(abs_video_path)
    meta_data = reader.get_meta_data()
    fps = meta_data['fps']
    
    # Henter frames fra videoen
    frames = []
    for i, frame in enumerate(reader):
        if i % skip_every_n_frames == 0: 
            frames.append(frame)
        
    # Opretter en midlertidig fil til at gemme GIF'en
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
        temp_gif_path = tmp_file.name
    
    # Gemmer som gif, med de indstilligner der er valgt
    imageio.mimsave(temp_gif_path, frames, fps=(fps / skip_every_n_frames * speed), loop=0)
    print(f"Saved GIF to {temp_gif_path}")
    
    base = os.path.basename(abs_video_path)
    base = os.path.splitext(base)[0] + ".gif"

    os.replace(temp_gif_path, os.path.join("temp", base)) # Flytter frame til temp mappen
    
    print("Successfully created output.gif")


def __from_image__(file_path):
    try:
        img = Image.open(file_path)

        base = os.path.basename(file_path)
        base = os.path.splitext(base)[0] + ".gif"

        destination_path = os.path.join("temp", base)

        img.save(destination_path, save_all=True, append_images=[img], loop=0) # Simpelt kovertering, så gemmes bare direkte
        
        print("Successfully created output.gif")
        
    except Exception as e:
        print(f"Error converting image: {str(e)}")


def __save_gif__(file_path):
    try: # Udvinder filnavn, ellers kopiers den bare
        base = os.path.basename(file_path)
        base = os.path.splitext(base)[0] + ".gif"

        destination_path = os.path.join("temp", base)

        shutil.copy2(file_path, destination_path)
        
        print(f"Moved {base} to temp directory")
        
    except Exception as e:
        print(f"Error saving gif: {str(e)}")