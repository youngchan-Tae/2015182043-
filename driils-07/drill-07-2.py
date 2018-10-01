from pico2d import *
open_canvas()
kpu = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
x = 0
frame = 0


while (x < 800):
    clear_canvas()
    kpu.draw(0, 0)
    character.clip_draw(frame * 100, 0, 100, 100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    x += 5
    delay(0.05)
    get_events()

close_canvas()