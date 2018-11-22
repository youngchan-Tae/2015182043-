from pico2d import *
import  game_framework
import  game_world

bef_state = None


#Penguin Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#Penguin action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

# Penguin Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, JUMP_TIMER = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
}


#Penguin States

class IdleState:

    @staticmethod
    def enter(penguin, event):
        if event == RIGHT_DOWN:
            penguin.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            penguin.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            penguin.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            penguin.velocity += RUN_SPEED_PPS

    @staticmethod
    def exit(penguin, event):
        global  bef_state
        bef_state = IdleState
        print(bef_state)

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
            penguin.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            penguin.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            penguin.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            penguin.velocity += RUN_SPEED_PPS
            penguin.dir = penguin.velocity

    @staticmethod
    def exit(penguin, event):
        global bef_state
        bef_state = RunState
        print(bef_state)

    @staticmethod
    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        penguin.x += penguin.velocity * game_framework.frame_time
        penguin.x = clamp(80, penguin.x, 800 - 80)

    @staticmethod
    def draw(penguin):
        penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 320, 100, 100, penguin.x, penguin.y)

class JumpState:
    def enter(penguin, event):
        penguin.Jump_Timer = get_time()
        penguin.collide = False

    def exit(penguin, event):
        penguin.collide = True

    def do(penguin):
        penguin.frame = (penguin.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if (get_time() - penguin.Jump_Timer) >= 1:
            penguin.add_event(JUMP_TIMER)

    def draw(penguin):
        penguin.image.clip_draw(int(penguin.frame) * 100 + 50, 125, 100, 100, penguin.x, penguin.y)

if bef_state == IdleState:
    next_state_table = {
        IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE_DOWN: JumpState},
        RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, SPACE_DOWN: JumpState},
        JumpState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, JUMP_TIMER: IdleState, SPACE_DOWN: JumpState}
        }
else:
    next_state_table = {
        IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                    SPACE_DOWN: JumpState},
        RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                   SPACE_DOWN: JumpState},
        JumpState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                    JUMP_TIMER: RunState, SPACE_DOWN: JumpState}
    }

class Penguin:

    def __init__(self):
        self.event_que = []
        self.x, self.y = 800 // 2, 90
        self.distance = 0
        self.image = load_image('penguin_animation.png')
        self.cur_state = IdleState
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.cur_state.enter(self, None)
        self.collide = False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.distance = self.distance + RUN_SPEED_PPS * game_framework.frame_time
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)



    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_penguin_place())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_penguin_place(self):
        return self.x - 40, self.y - 50, self.x + 30, self.y + 50