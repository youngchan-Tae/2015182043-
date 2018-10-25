import random
import json
import os

from pico2d import *

import game_framework
import title_state

from background import Background
from penguin import Penguin

name = "MainState"

penguin = None
background = None
font = None


def enter():
    global penguin, background
    penguin = Penguin()
    background = Background()


def exit():
    global penguin, background
    del penguin
    del background



def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        else:
            penguin.handle_event(event)



def update():
    penguin.update()

def draw():
    clear_canvas()
    background.draw()
    penguin.draw()
    update_canvas()





