from pico2d import *
import game_framework
import game_world
import main_state
from obstacle import Obstacle



#Penguin Left, Right Speed
PIXEL_PER_METER_LR = (10.0 / 0.3)
RUN_SPEED_KMPH_LR = 20.0
RUN_SPEED_MPM_LR = (RUN_SPEED_KMPH_LR * 1000.0 / 60.0)
RUN_SPEED_MPS_LR = (RUN_SPEED_MPM_LR / 60.0)
RUN_SPEED_PPS_LR = (RUN_SPEED_MPS_LR * PIXEL_PER_METER_LR)


#Penguin Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


#Penguin action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Penguin Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, SPACE_UP, JUMP_TIMER = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP
}

#Penguin States
class RunState:
    @staticmethod
    def enter(penguin, event):
        if event == RIGHT_DOWN:
            penguin.velocity += RUN_SPEED_PPS_LR
        elif event == LEFT_DOWN:
            penguin.velocity -= RUN_SPEED_PPS_LR
        elif event == RIGHT_UP:
            penguin.velocity -= RUN_SPEED_PPS_LR
        elif event == LEFT_UP:
            penguin.velocity += RUN_SPEED_PPS_LR
        penguin.dir = penguin.velocity

    @staticmethod
    def exit(penguin, event):
        penguin.collide_frame = 0

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        penguin.collide_frame = (penguin.collide_frame + ACTION_PER_TIME * game_framework.frame_time) % 3
        penguin.x += penguin.velocity * game_framework.frame_time * main_state.collide_state
        penguin.x = clamp(80, penguin.x, 800 - 80)


    @staticmethod
    def draw(penguin):
        if main_state.collide_state == 0:
            if main_state.penguin_collide_dir == 0:
                penguin.image.clip_draw(450, 125, 100, 100, penguin.x - int(penguin.collide_frame) * 30 + 90, penguin.y)
            else:
                penguin.image.clip_draw(550, 125, 100, 100, penguin.x + int(penguin.collide_frame) * 30 - 90, penguin.y)
        else:
            if main_state.item_eat == True:
                penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 225, 100, 90, penguin.x, penguin.y)
            else:
                penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 320, 100, 100, penguin.x, penguin.y)


class JumpState:
    @staticmethod
    def enter(penguin, event):
        penguin.Jump_Timer = get_time()
        penguin.jump_collide = False

    @staticmethod
    def exit(penguin, event):
        penguin.jump_collide = True

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if (get_time() - penguin.Jump_Timer) >= 1:
            penguin.add_event(JUMP_TIMER)

    @staticmethod
    def draw(penguin):
        if main_state.item_eat == True:
            penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 25, 100, 100, penguin.x, penguin.y)
        else:
            penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 125, 100, 100, penguin.x, penguin.y)

next_state_table = {
    RunState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SPACE_DOWN: JumpState, SPACE_UP: RunState},
    JumpState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                    JUMP_TIMER: RunState, SPACE_DOWN: JumpState, SPACE_UP: RunState}
}

class Penguin:

    def __init__(self):
        self.event_que = []
        self.x, self.y = 800 // 2, 90
        self.distance = 0
        self.image = load_image('penguin_animation.png')
        self.cur_state = RunState
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.collide_frame = 0
        self.cur_state.enter(self, None)
        self.jump_collide = True
        self.font = load_font('ENCR10B.TTF', 25)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.distance = self.distance + RUN_SPEED_PPS * game_framework.frame_time * main_state.collide_state
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        #print(self.velocity)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(10, 520, 'Speed: %d ' % RUN_SPEED_KMPH, (0, 0, 0))
        self.font.draw(400, 570, 'Distance: %d / 20000' % self.distance, (0, 0, 0))

    def handle_event(self, event):
        if main_state.collide_state == 1:
            if (event.type, event.key) in key_event_table:
                key_event = key_event_table[(event.type, event.key)]
                self.add_event(key_event)

    def get_bb(self):
        return self.x - 35, self.y - 50, self.x + 25, self.y - 20