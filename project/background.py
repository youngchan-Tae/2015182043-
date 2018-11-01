from pico2d import *


class Background:
    def __init__(self):
        self.image_draw = 0
        if self.image_draw == 0:
            self.image = load_image('project_background0.png')
        elif self.image_draw == 1:
            self.image = load_image('project_background1.png')
        elif self.image_draw == 2:
            self.image = load_image('project_background2.png')

    def update(self):
        ++self.image_draw
        self.image_draw = (self.image_draw) / 4

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, 400, 300)
