from pico2d import *

class Background:
    image = None

    def __init__(self):
        self.image = load_image('project_background.png')

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, 400, 300)
