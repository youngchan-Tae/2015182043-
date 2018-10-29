from pico2d import *

import  game_world

# Penguin Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE= range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

#Pengguin States

class IdleState:

    @staticmethod
    def enter(penguin, event):
        if event == RIGHT_DOWN:
            penguin.velocity += 1
        elif event == LEFT_DOWN:
            penguin.velocity -= 1
        elif event == RIGHT_UP:
            penguin.velocity -= 1
        elif event == LEFT_UP:
            penguin.velocity += 1

    @staticmethod
    def exit(penguin, event):
        if event == SPACE:
            pass

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + 1) % 7

    @staticmethod
    def draw(penguin):
        penguin.image.clip_draw(penguin.frame * 100 + 50, 300, 100, 100, penguin.x, penguin.y)




class RunState:

    @staticmethod
    def enter(penguin, event):
        def enter(penguin, event):
            if event == RIGHT_DOWN:
                penguin.velocity += 1
            elif event == LEFT_DOWN:
                penguin.velocity -= 1
            elif event == RIGHT_UP:
                penguin.velocity -= 1
            elif event == LEFT_UP:
                penguin.velocity += 1
            penguin.dir = penguin.velocity

    @staticmethod
    def exit(penguin, event):
        if event == SPACE:
            pass

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + 1) % 7
        penguin.x = clamp(25, penguin.x, 1600 - 25)

    @staticmethod
    def draw(penguin):
        penguin.image.clip_draw(penguin.frame * 100 + 50, 300, 100, 100, penguin.x, penguin.y)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState}
}


class Penguin:

    def __init__(self):
        self.event_que = []
        self.x, self.y = 800 // 2, 90
        self.image = load_image('penguin_animation.png')
        self.cur_state = IdleState
        self.dir = 1
        self.velocity = 0
        self.enter_state[IDLE](self)



    # IDLE state functions
    def enter_IDLE(self):
        self.frame = 0

    def exit_IDLE(self):
        pass

    def do_IDLE(self):
        self.frame = (self.frame + 1) % 7

    def draw_IDLE(self):
        self.image.clip_draw(self.frame * 100 + 50, 300, 100, 100, self.x, self.y)

    # RUN state functions
    def enter_RUN(self):
        self.frame = 0
        self.dir = self.velocity

    def exit_RUN(self):
        pass

    def do_RUN(self):
        self.frame = (self.frame + 1) % 7
        self.x += self.velocity
        self.x = clamp(25, self.x, 800-25)

    def draw_RUN(self):
        self.image.clip_draw(self.frame * 100 + 50, 300, 100, 100, self.x, self.y)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def change_state(self, state):
        self.exit_state[self.cur_state](self)
        self.enter_state[state](self)
        self.cur_state = state

    def update(self):
        self.do_state[self.cur_state](self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(next_state_table[self.cur_state][event])


    def draw(self):
        self.draw_state[self.cur_state](self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == RIGHT_DOWN:
                self.velocity += 1
            elif key_event == LEFT_DOWN:
                self.velocity -= 1
            elif key_event == RIGHT_UP:
                self.velocity -= 1
            elif key_event == LEFT_UP:
                self.velocity += 1
            self.add_event(key_event)

