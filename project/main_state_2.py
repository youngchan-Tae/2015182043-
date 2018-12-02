import random
import json
import os

from pico2d import *

import game_framework
import game_world
import penguin

from background import Background2
from penguin import Penguin
from obstacle import Obstacle

name = "MainState"

penguin = None
background2 = None
obstacle = None
font = None
collide_state = 1

global collide_judge
global collide_timer
collide_timer = 0
collide_judge = 0


def enter():
    global penguin, background2, obstacle
    penguin = Penguin()
    background2 = Background2()
    obstacle = Obstacle()

    game_world.add_object(obstacle, 1)
    game_world.add_object(background2, 0)
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
    global obstacle
    global collide_state
    global collide_timer
    global collide_judge


    if (penguin.distance % 100 > 99.5): # 일정거리마다 장애물 생성
        obstacle = Obstacle()
        game_world.add_object(obstacle, 1)

    for game_object in game_world.all_objects():
        game_object.update()
    if collide_judge == 0:
        if collide(penguin, obstacle):
            collide_state = 0 # 현재 충돌상태(시간정지)
            collide_judge = 1 # 충돌 면역 켜짐
            print(collide_timer)
            if (obstacle.x < penguin.x):
               penguin.x += 90
            elif (obstacle.x > penguin.x):
               penguin.x -= 90
    if get_time() - collide_timer > 1:
        collide_state = 1 #충돌상태(시간정지) 해제
        collide_judge = 0 # 충돌 면역 꺼짐





    ####################
    # ###############################

    # 펭귄 충돌시 시간 정지 변수

    ###################################################

    # 펭귄 충돌시 좌우로 밀림
    ###################################################


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