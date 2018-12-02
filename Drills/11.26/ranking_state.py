import random
import json
import pickle
import os

import boy
from pico2d import *
import game_framework
import game_world
import world_build_state
import main_state

name = "RankingState"


def enter():
    global boy
    global font
    font = load_font('ENCR10B.TTF', 20)
    hide_cursor()
    hide_lattice()

def exit():
    pass

def pause():
    pass



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world_build_state)

def update():
    pass

def draw():
    clear_canvas()
    font.draw(500, 400, '(rank %f = Time: %3.2f)' % (1, 100), (0, 0, 0))
    update_canvas()






