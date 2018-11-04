import random
import json
import os

from pico2d import *

import game_framework
import game_world

from background import Background0
from background import Background1
from background import Background2
from penguin import Penguin

name = "MainState"

penguin = None
background = None
font = None


def enter():
    global penguin, background
    penguin = Penguin()
    background = Background0()
    game_world.add_object(background, 0)
    game_world.add_object(penguin, 1)


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
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()





