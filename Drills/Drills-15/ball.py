import random
from pico2d import *
import game_world
import game_framework
import boy
import background

class Ball:
    image = None

    def __init__(self, background):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.fall_speed = random.randint(0, 1800), random.randint(0, 1100), 0
        self.bg = background


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.draw(self.x - self.bg.window_left, self.y - self.bg.window_bottom)

    def update(self):
        self.y -= self.fall_speed * game_framework.frame_time

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

        #수정완료료

