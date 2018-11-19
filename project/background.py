from pico2d import *
import  game_framework
import  game_world


TIME_PER_MOVE = 0.5
MOVE_PER_TIME = 1.0 / TIME_PER_MOVE
FRAMES_PER_MOVE = 7


class Background:
    def __init__(self):
        self.image = load_image('project_background.png')
        self.frame = 0
    def update(self):
        self.frame = (self.frame + 1 + FRAMES_PER_MOVE  * MOVE_PER_TIME * game_framework.frame_time ) % 2

    def draw(self):
        self.image.clip_draw(800 * self.frame, 0, 800, 600, 400, 300)



