from PIL import Image, ImageDraw, ImageFont
import imageio, math, os
import numpy as np

WIDTH = 700
CAPTION_HEIGHT = 100
MAX_CHARACTERS = 8

FONT_SIZE = 70

def add_caption_to_gif(gif_path, caption):
    # Load the GIF using imageio
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


    words = caption.split()
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
    caption_image = Image.new('RGB', (WIDTH, CAPTION_HEIGHT * caption_scale), color='white')
    draw = ImageDraw.Draw(caption_image)

    # Choose a font and size
    try:
        font_path = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'Futura Extra Black Condensed Regular.otf')
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
        draw.text((text_x, text_y), lines[i], font=font, fill='black')


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
        new_frame = Image.new('RGB', (gif_width, gif_height + CAPTION_HEIGHT * caption_scale))
        new_frame.paste(frame_image, (0, CAPTION_HEIGHT * caption_scale))
        new_frame.paste(caption_image, (0, 0))

        # Convert the new frame back to a numpy array and add to the list
        modified_frames.append(np.array(new_frame))

    # Save the modified GIF
    output_path = 'output_with_caption.gif'
    imageio.mimsave(output_path, modified_frames, duration=0.1, loop=0)

    return output_path

if __name__ == "__main__":
    gif_path = r'C:\Users\bertr\OneDrive\Skrivebord\gif-tool-local\output\output.gif'
    caption = 'jeg elsker blåbær der er store'
    add_caption_to_gif(gif_path, caption)
