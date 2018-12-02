from pico2d import *
import game_framework
import game_world
import background
import random
import main_state

class Obstacle:
    def __init__(self):
        self.image = load_image('project_obstacle.png')
        self.frame = 0
        self.x, self.y = random.randint(380, 420), 300
        self.obstacle_direct = random.randint(-45, 45)

    def update(self):
        self.frame = (self.frame + background.FRAMES_PER_ACTION * background.ACTION_PER_TIME * game_framework.frame_time)
        if (self.frame > 5):
            self.frame = 4
        if main_state.collide_state == 0:
            self.obstacle_direct = 0

        self.y = self.y -  background.FRAMES_PER_ACTION * background.ACTION_PER_TIME * game_framework.frame_time * 50
        self.x = self.x -  background.FRAMES_PER_ACTION * background.ACTION_PER_TIME * game_framework.frame_time * self.obstacle_direct

        if self.y < -50:
            game_world.remove_object(self)


    def draw(self):
        if(main_state.collide_state == 0):
            self.image.clip_draw(160 * int(self.frame), 500, 160, 100, self.x, 50)
        else:
            self.image.clip_draw(160 * int(self.frame), 500, 160, 100, self.x, self.y )


    def get_bb(self):
        return self.x - 60, self.y - 18, self.x + 60, self.y +8