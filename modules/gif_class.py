from PIL import Image
import os, imageio

class GifHolder:
    def __init__(self, gif_path):
        self.path = gif_path

        self.name = ""
        
        self.clip_duration = 0
        self.frames = 0
        self.fps = 0
        self.space = 0
        
        self.width = 0
        self.height = 0
        
        self.populate_gif_info()

    def populate_gif_info(self): # Intern funktion til at hente metadata fra gif'en og gemme som variabler
        try:
            # Åbner gif'en og henter dens metadata
            gif_reader = imageio.get_reader(self.path)
            
            durations = []
            for frame_idx in range(len(gif_reader)):
                durations.append(gif_reader.get_meta_data(frame_idx).get('duration', 1000) / 1000)
            gif_reader.close()
            

            temp_gif = Image.open(self.path)
            
            
            # Gemmer metadatas i variablerne
            self.name = os.path.basename(self.path)
            
            
            self.clip_duration = sum(durations)  # Convert to seconds
            self.frames = len(durations)
            self.fps =  self.frames/ self.clip_duration
            
            
            self.width, self.height = temp_gif.size
            
            
            self.space = os.path.getsize(self.path) / (1024 * 1024)  # Laver til MB

        except Exception as e:
            print(f"Error populating GIF info: {str(e)}")

    def __str__(self):
        return f"GifHolder: {self.name}, Duration: {self.name}ms, FPS: {self.name}, Size: {self.width}x{self.height}"