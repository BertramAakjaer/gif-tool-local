from PIL import Image
import os

class GifHolder:
    def __init__(self, gif_path):


        self.path = gif_path

        self.name = ""
        #self.clip_duration = 0
        #self.frames = 0
        self.width = 0
        self.height = 0
        
        #self.fps = 0
        
        self.space = 0

        self.populate_gif_info()

    def populate_gif_info(self):
        try:
            temp_gif = Image.open(self.path)
            self.name = os.path.basename(self.path)
            #self.clip_duration, self.frames = self.get_average_duration()
            
            #self.fps = 1 / self.clip_duration
            
            self.width, self.height = temp_gif.size
            
            self.space = os.path.getsize(self.path) / (1024 * 1024)  # Convert bytes to MB

        except Exception as e:
            print(f"Error populating GIF info: {str(e)}")
        
    def get_average_duration(self):
        gif = Image.open(self.path)

        total_frames = gif.n_frames

        durations = []
        for frame in range(total_frames):
            gif.seek(frame)
            durations.append(gif.info['duration'])

        average_duration = sum(durations) / len(durations)
        return average_duration, len(total_frames)

    def __str__(self):
        return f"GifHolder: {self.name}, Duration: {self.name}ms, FPS: {self.name}, Size: {self.width}x{self.height}"