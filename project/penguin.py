from pico2d import *
import  game_framework
import  game_world

#Penguin Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#Penguin action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Penguin Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, SPACE_UP, JUMP_TIMER, No_Key= range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP,
    (SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT) : No_Key,
    (SDL_KEYDOWN, SDLK_SPACE, SDLK_LEFT) : No_Key,
    (SDL_KEYUP, SDLK_SPACE, SDLK_RIGHT) : No_Key,
    (SDL_KEYUP, SDLK_SPACE, SDLK_LEFT) : No_Key
}

#Penguin States

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
        pass

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

    @staticmethod
    def draw(penguin):
        penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 320, 100, 100, penguin.x, penguin.y)




class RunState:

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
        penguin.dir = penguin.velocity

    @staticmethod
    def exit(penguin, event):
        pass

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        penguin.x += penguin.velocity
        penguin.x = clamp(25, penguin.x, 800 - 25)

    @staticmethod
    def draw(penguin):
        penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 320, 100, 100, penguin.x, penguin.y)

class JumpState:
    def enter(penguin, event):
        penguin.Jump_Timer = get_time()

    def exit(penguin, event):
        pass

    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if (get_time() - penguin.Jump_Timer) >= 1:
            penguin.add_event(JUMP_TIMER)

    def draw(penguin):
        penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 125, 100, 100, penguin.x, penguin.y)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE_DOWN: JumpState, SPACE_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, SPACE_DOWN: JumpState, SPACE_UP: RunState},
    JumpState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, JUMP_TIMER: IdleState, SPACE_DOWN: JumpState, SPACE_UP: JumpState}
}


class Penguin:

    def __init__(self):
        self.event_que = []
        self.x, self.y = 800 // 2, 90
        self.image = load_image('penguin_animation.png')
        self.cur_state = IdleState
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.cur_state.enter(self, None)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
