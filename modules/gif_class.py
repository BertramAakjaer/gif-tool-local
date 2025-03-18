from PIL import Image
import os

class GifHolder:
    def __init__(self, gif_path):


        self.path = gif_path

        self.name = ""
        #self.duration = 0
        #self.fps = 0
        self.width = 0
        self.height = 0

        self.populate_gif_info()

    def populate_gif_info(self):
        try:
            temp_gif = Image.open(self.path)
            self.name = os.path.basename(self.path)
            #self.duration = temp_gif.info["duration"]
            #self.fps = 1000 / self.duration
            self.width, self.height = temp_gif.size

        except Exception as e:
            print(f"Error populating GIF info: {str(e)}")

    def __str__(self):
        return f"GifHolder: {self.name}, Duration: {self.name}ms, FPS: {self.name}, Size: {self.width}x{self.height}"