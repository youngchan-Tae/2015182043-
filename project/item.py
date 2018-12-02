from pico2d import *
import game_framework
import game_world
import background
import random
import main_state

class Item:
    def __init__(self):
        self.image = load_image('project_item.png')
        self.x, self.y = random.randint(380, 420), 300
        self.obstacle_direct = random.randint(-45, 45)

    def update(self):
        self.y = self.y -  background.FRAMES_PER_ACTION * background.ACTION_PER_TIME * game_framework.frame_time * 50 * main_state.collide_state
        self.x = self.x -  background.FRAMES_PER_ACTION * background.ACTION_PER_TIME * game_framework.frame_time * self.obstacle_direct * main_state.collide_state

        if self.y < -50:
            game_world.remove_object(self)


    def draw(self):
            self.image.draw(self.x, self.y + 50)


    def get_bb(self):
        return self.x - 60, self.y - 18, self.x + 60, self.y +8