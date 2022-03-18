import pygame
import os
import math
CAR_IMG = pygame.image.load(os.path.join("src\\img", "car.png" ))
BALL_IMG = pygame.image.load(os.path.join("src\\img", "ball.png" ))
IMG = BALL_IMG
MAX_SPEED = 0.8

def scalar(vect1, vect2):
    return (vect1[0] * vect2[1]) - (vect1[1] * vect2[0])
def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])
def div(p1, p2):
    if p2[1] == 0: return 0
    return (p1[0] / p2[0], p1[1] / p2[1])
def mult(p1, p2):
    return (p1[0] * p2[0], p1[1] * p2[1])
def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])
class Car:
    def __init__(self, x, y, angl):
        self.x = int(x)
        self.y = int(y)
        self.width = IMG.get_size()[0]/2
        self.height = IMG.get_size()[1]/2
        self.speed = 0
        self.acc = 0
        self.__angle = angl
        self.driftAngle = 0
        self.crashed = False

        self.xVel = 0
        self.yVel = 0
    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angl):
        self.__angle = angl
        if abs(self.__angle) >= 360:
            self.__angle = 0
        
    def draw_shadow(self, win, color):
        #rotate the img
        rotated_image = pygame.transform.rotate(IMG, -self.__angle)
        #create img frame
        new_rect = rotated_image.get_rect(center = IMG.get_rect(topleft = (self.x, self.y)).center)
        #shadow the image
        r, g, b = color

        w, h = rotated_image.get_size()
        for x in range(w):
            for y in range(h):
                a = rotated_image.get_at((x, y))[3]
                rotated_image.set_at((x, y), pygame.Color(r, g, b, a))

        win.blit(rotated_image, new_rect.topleft)

    def draw(self, win):
        #rotate the img
        rotated_image = pygame.transform.rotate(IMG, -self.__angle)
        new_rect = rotated_image.get_rect(center = IMG.get_rect(topleft = (self.x, self.y)).center)
        w, h = rotated_image.get_size()
        win.blit(rotated_image, new_rect.topleft)
        
    def move(self):
        if abs(self.acc) == 1:
            if abs(self.speed) < 10:
                self.speed += self.acc * -0.8 #i say minus because i wanna flip direction
            if abs(self.speed) < 0.01:
                self.speed = 0
                return
        self.xVel += math.cos(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc
        self.yVel += math.sin(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc #acc => dopredu|dozadu

        self.angle += self.driftAngle * self.speed * -0.1

        self.x += self.xVel
        self.y += self.yVel
        self.driftAngle *= 0.85
        self.xVel *= 0.93
        self.yVel *= 0.93
        self.speed *= 0.93

    def rotateBy(self, angl):
        if abs(self.driftAngle) < 5 - angl/5:
            self.driftAngle += angl/5
        elif angl > 0:
            self.driftAngle = 5
        else:
            self.driftAngle = -5

        
    def visionPoints(self, road):
        pass
    def visionDistance(self, road):
        pass

    def cross(self, a1, a2, b1, b2):
        pass


    def collides(self,road):
        pass

