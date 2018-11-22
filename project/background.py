from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Background:
    def __init__(self):
        self.image = load_image('project_background.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time ) % 6

    def draw(self):
        self.image.clip_draw(800 * int(self.frame), 0, 800, 600, 400, 300)



