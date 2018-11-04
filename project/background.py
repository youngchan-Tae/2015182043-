from pico2d import *


class Background0:
    def __init__(self):
        self.image = load_image('project_background.png')
        self.frame = 0
    def update(self):
        frame = (frame + 1) % 2

    def draw(self):
        self.image.clip_draw(400*, 0, 800, 600, 400, 300)



