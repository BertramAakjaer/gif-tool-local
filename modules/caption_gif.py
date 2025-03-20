from PIL import Image, ImageDraw, ImageFont
import imageio, os, tempfile
import numpy as np

WIDTH = 400
CAPTION_HEIGHT = int(WIDTH / 8)
MAX_CHARACTERS = 20

FONT_SIZE = 40

FILE_ADD_NAME = '_captioned'

def add_caption_to_gif(gif_path, caption, n_duration=0.1):
    gif = imageio.mimread(gif_path)

    # Determine the size of the GIF
    gif_width, gif_height = gif[0].shape[1], gif[0].shape[0]

    # Reszing gif to a specific width, but keeping the aspect ratio
    scale = WIDTH / gif_width
    gif_width = int(gif_width * scale)
    gif_height = int(gif_height * scale)
    gif = [np.array(Image.fromarray(frame).resize((gif_width, gif_height))) for frame in gif]

    # saving rezied gif
    imageio.mimsave(r"temp\resized_for_caption.gif", gif) 
    
    # caption_scale = math.ceil(len(caption) / MAX_CHARACTERS)


    words = caption.split(" ")
    lines = []

    for i in range(len(words)):
        if lines == []:
            lines.append(words[i])
            continue
        
        if len(lines[-1] + ' ' + words[i]) <= MAX_CHARACTERS:
            lines[-1] = (lines[-1] + ' ' + words[i])
            continue
        else:
            lines.append(words[i])
    
    caption_scale = len(lines)

    # Create a blank image with white background for the caption
    caption_image = Image.new('RGB', (WIDTH, CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT), color='white')
    draw = ImageDraw.Draw(caption_image)

    # Choose a font and size
    try:
        font_path = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'Futura Extra Black Condensed Regular.otf')
        print(font_path)
        font = ImageFont.truetype(font_path, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default(FONT_SIZE)




    for i in range(caption_scale):
        # Calculate the size of the text
        bbox = draw.textbbox((0, i * CAPTION_HEIGHT), lines[i], font=font, align='center')
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate the position to center the text
        text_x = (WIDTH - text_width) / 2
        text_y = i * CAPTION_HEIGHT

        # Add the text to the caption image
        draw.text((text_x, text_y + CAPTION_HEIGHT / 2), lines[i], font=font, fill='black')


    # Convert the caption image to a numpy array
    caption_array = np.array(caption_image)

    gif = imageio.mimread(r"temp\resized_for_caption.gif")

    # Create a list to hold the modified frames
    modified_frames = []

    # Add the caption to each frame of the GIF
    for frame in gif:
        # Convert the frame to a PIL Image
        frame_image = Image.fromarray(frame)

        # Create a new image with extra space for the caption
        new_frame = Image.new('RGB', (gif_width, gif_height + CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT))
        new_frame.paste(frame_image, (0, CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT))
        new_frame.paste(caption_image, (0, 0))

        # Convert the new frame back to a numpy array and add to the list
        modified_frames.append(np.array(new_frame))

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
        temp_gif_path = tmp_file.name
    
    imageio.mimsave(temp_gif_path, modified_frames, duration=n_duration, loop=0, format='GIF')
    
    base = os.path.basename(gif_path)
    base = os.path.splitext(base)[0] + FILE_ADD_NAME + '.gif'
    
    path_to_gif = os.path.join("temp", base)
    
    os.replace(temp_gif_path, path_to_gif)
    
    return path_to_gif