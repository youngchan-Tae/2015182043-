import random
import json
import os

from pico2d import *

import game_framework
import game_world
import penguin

from background import Background
from penguin import Penguin
from obstacle import Obstacle

name = "MainState"

penguin = None
background = None
obstacle = None
font = None


def enter():
    global penguin, background, obstacle
    penguin = Penguin()
    background = Background()


    game_world.add_object(background, 0)
    game_world.add_object(penguin, 2)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()


    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            penguin.handle_event(event)




def update():
    if (penguin.distance % 100 > 99): # 일정거리마다 장애물 생성
        print(penguin.distance % 100)
        obstacle = Obstacle()
        game_world.add_object(obstacle, 1)
    for game_object in game_world.all_objects():
        game_object.update()






def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_penguin_place()
    left_b, bottom_b, right_b, top_b = b.get_obstacle_place()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True