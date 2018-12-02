import random
import json
import os

from pico2d import *

import end_state
import game_framework
import game_world
import penguin

penguin.RUN_SPEED_KMPH = 10

from background import Background
from penguin import Penguin
from obstacle import Obstacle
from item import  Item

name = "MainState"

penguin = None
background = None
obstacle = None
item = None
font = None
collide_state = 1

global collide_judge
global collide_timer
global penguin_collide_dir
penguin_collide_dir = 0
collide_timer = 0
collide_judge = 0
item_eat = False

def enter():
    global penguin, background, obstacle, item
    penguin = Penguin()
    background = Background()
    obstacle = Obstacle()
    item = Item()

    game_world.add_object(obstacle, 1)
    game_world.add_object(item, 1)
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
    global penguin
    global obstacle
    global background
    global item
    global collide_state
    global collide_timer
    global collide_judge
    global penguin_collide_dir
    global item_eat

    if (penguin.distance % 100 > 99.6):
        item = Item()
        game_world.add_object(item, 1)

    if (penguin.distance % 100 > 99.6): # 일정거리마다 장애물 생성
        obstacle = Obstacle()
        game_world.add_object(obstacle, 1)


    for game_object in game_world.all_objects():
        game_object.update()

    if collide_judge == 0:
        if collide(penguin, obstacle):
            collide_state = 0 # 현재 충돌상태(시간정지)
            collide_judge = 1 # 충돌 면역 켜짐
            item_eat = False
            if (obstacle.x < penguin.x):
               penguin.x += 90
               penguin_collide_dir = 1
            elif (obstacle.x >= penguin.x):
               penguin.x -= 90
               penguin_collide_dir = 0

    elif get_time() - collide_timer > 1:
        collide_state = 1 #충돌상태(시간정지) 해제
        collide_judge = 0 # 충돌 면역 꺼짐

    elif collide_judge == 1:
        collide_state = 0

    if penguin.jump_collide == True:
        if collide(penguin, item):
            game_world.remove_object(item)
            item_eat = True
    print(penguin.distance)

    if penguin.distance >= 20000:
        game_framework.change_state(end_state)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    global penguin
    global collide_timer
    global collide_state
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if (right_a <= left_b) or (penguin.jump_collide == False): return False
    if (left_a >= right_b) or (penguin.jump_collide == False): return False
    if (top_a <= bottom_b) or (penguin.jump_collide == False): return False
    if (bottom_a >= top_b) or (penguin.jump_collide == False): return False

    collide_timer = get_time()
    return True