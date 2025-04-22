from PIL import Image, ImageDraw, ImageFont
import imageio, os, tempfile
import numpy as np



# Indstillinger til brugeren
WIDTH = 400
CAPTION_HEIGHT = int(WIDTH / 8)
MAX_CHARACTERS = 20

FONT_SIZE = 40





FILE_ADD_NAME = '_captioned'



# Function til at kaldes fra andre steder
def add_caption_to_gif(gif_path, caption):    
    gif_reader = imageio.get_reader(gif_path) # Til metadata fra gif'en, for at bevare "frame duration"

    
    # Henter duration mellem billederne på en per, billede basis
    durations = []
    for frame_idx in range(len(gif_reader)):
        durations.append(gif_reader.get_meta_data(frame_idx).get('duration', 1000) / 1000)
    
    gif = list(gif_reader) # Henter alle frames fra gif'en
    gif_reader.close() # Lukker gif'en
    

    # Ud fra den første frame, henter vi width og height
    gif_width, gif_height = gif[0].shape[1], gif[0].shape[0]

    # Rezier vores nuværende gif til den ønskede bredde, hvor ratio'en beholder, så captionen passer ind
    # Dette gør så teksten ikke bliver for lille, og at det ser pænt ud
    # Dog kan det øge hvor meget en gif fylder, da vi reizer (enten opad eller nedad)
    
    scale = WIDTH / gif_width
    gif_width = int(gif_width * scale)
    gif_height = int(gif_height * scale)
    gif = [np.array(Image.fromarray(frame).resize((gif_width, gif_height))) for frame in gif]
    
    
    # Opretter en midlertidig fil til at gemme den resized gif, så vores program ikke bliver forvirret over en korrupt fil
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
        temp_gif_path = tmp_file.name

    # Gemmer den resized gif til den midlertidige fil
    imageio.mimsave(temp_gif_path, gif) 




    # Følgende kode udregner hvor mange linjer der skal bruges, og tager input teskten og deler den op i de linjer
    # Her er det som en liste, hvor hvert element er en linje, med det tilhørende tekst
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
    
    caption_scale = len(lines) # Det antal linjer der benyttes


    # Da baggrunden til vores caption er hvid, laves en hvid baggrund
    caption_image = Image.new('RGB', (WIDTH, CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT), color='white')
    draw = ImageDraw.Draw(caption_image)

    # Prøver at bruge vores custom font, der er tit bruges til memes
    try:
        font_path = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'Futura Extra Black Condensed Regular.otf')
        print(font_path)
        font = ImageFont.truetype(font_path, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default(FONT_SIZE) # Falder tilbage til den hvis den anden ikke findes



    # Itterer over hver linje i vores caption
    for i in range(caption_scale):
        # Udregner størrelsen på det område, hvor teksten skal være
        bbox = draw.textbbox((0, i * CAPTION_HEIGHT), lines[i], font=font, align='center')
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Centerer teksten
        text_x = (WIDTH - text_width) / 2
        text_y = i * CAPTION_HEIGHT

        # Sætter det sammen og putter på den hvide baggrund
        draw.text((text_x, text_y + CAPTION_HEIGHT / 2), lines[i], font=font, fill='black')


    # Omdanner vores caption image til en numpy array, da resten af gif'en er det
    caption_array = np.array(caption_image)

    gif = imageio.mimread(temp_gif_path)
    
    os.unlink(temp_gif_path) # Frigøre den midlertidige fil, så den ikke fylder mere end nødvendigt


    # Opretter en liste til den sammensatte gif
    modified_frames = []

    for frame in gif:
        # Laver hvert billede til PIL format
        frame_image = Image.fromarray(frame)

        # Opretter et enkelt billede med ekstra plads til caption'en
        new_frame = Image.new('RGB', (gif_width, gif_height + CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT))
        new_frame.paste(frame_image, (0, CAPTION_HEIGHT * caption_scale + CAPTION_HEIGHT))
        new_frame.paste(caption_image, (0, 0))

        # omdanner tilbage til numpy array og tilføjer det til de nye frames
        modified_frames.append(np.array(new_frame))

    # Opretter en midlertidig fil til at gemme den resized gif, så vores program ikke bliver forvirret over en korrupt fil
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp_file:
        temp_gif_path = tmp_file.name
    
    # Gemmer den resized gif til den midlertidige fil
    imageio.mimsave(temp_gif_path, modified_frames, duration=durations, loop=0, format='GIF')
    
    
    
    base = os.path.basename(gif_path)
    base = os.path.splitext(base)[0] + FILE_ADD_NAME + '.gif'
    
    path_to_gif = os.path.join("temp", base)
    
    
    # Flytter den midlertidige fil til den ønskede placering
    os.replace(temp_gif_path, path_to_gif)
    
    return path_to_gif # Returnerer stien til den nye gif