import pygame
import os
CAR_IMG = pygame.image.load(os.path.join("src\\img", "car.png" ))
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
        self.width = CAR_IMG.get_size()[0]/2
        self.height = CAR_IMG.get_size()[1]/2
        self.speed = 0
        self.acc = 0
        self.__angle = angl
        self.driftAngle = 0
        self.crashed = False
        
    
        
    def drawShadow(self, win, color):
        pass
    def draw(self, win):
        pass
        
    def move(self):
        pass

        
    def rotateBy(self, angl):
        pass
    def visionPoints(self, road):
        pass
    def visionDistance(self, road):
        pass

    def cross(self, a1, a2, b1, b2):
        pass


    def collides(self,road):
        pass

