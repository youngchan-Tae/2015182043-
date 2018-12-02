from pico2d import *
import game_framework
import game_world
import main_state


TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Background:
    def __init__(self):
        self.image = load_image('project_background.png')
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 25)
        self.bgm = load_music('background_sound.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * main_state.collide_state ) % 6
    def draw(self):
        self.image.clip_draw(800 * int(self.frame), 0, 800, 600, 400, 300)
        self.font.draw(10, 570, 'PlayTime: %3.2f second' % get_time(), (0, 0, 0))

class Background2:
    def __init__(self):
        self.image = load_image('project_background2.png')
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 25)
        self.bgm = load_music('background_sound.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * main_state.collide_state ) % 6
    def draw(self):
        self.image.clip_draw(800 * int(self.frame), 0, 800, 600, 400, 300)
        self.font.draw(10, 570, 'PlayTime: %3.2f second' % get_time(), (0, 0, 0))

