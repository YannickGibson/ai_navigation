

from app.src.car.car import Car
import pygame

def test_init():
    c = Car(0, 0, 0)
    assert(c.acc == 0)
    assert(c.sight == 400)
    assert(c.angle == 0)
    assert(c.center == None)

def test_draw_shadow():
    c = Car(0, 0, 0)
    win = pygame.display.set_mode((100,100),flags=pygame.HIDDEN)
    assert((0, 0, 0, 255) == win.get_at((0,0)))
    c.draw_shadow(win, [255, 0, 255])
    assert((255, 0, 255, 255) == win.get_at((1,1)))

def test_draw():
    c = Car(0, 0, 0)
    win = pygame.display.set_mode((100,100),flags=pygame.HIDDEN)
    assert((0, 0, 0, 255) == win.get_at((0,0)))
    c.draw(win)
    assert((255, 255, 255, 255) == win.get_at((1,1)))
