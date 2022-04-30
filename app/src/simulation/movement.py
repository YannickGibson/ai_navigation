import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from abc import abstractmethod
from app.src.car.car import Car, add, sub, normalize
import pickle
import math
import pygame
import sys
from app.src.simulation.base import Simulation


#WIN_WIDTH = 1540
#WIN_HEIGHT = 750
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class MovementSimulation(Simulation):
    def __init__(self, road_index):
        super().__init__(road_index)
    def _draw(self):
        #background
        if self.car.collides(self.road):
            self.win.fill((255,0,0))
        else:
            self.win.fill((0,0,0))
        
        # road
        pygame.draw.polygon(self.win, (255,255,255), self.road[0] + self.road[1])
        
        #fitness lines
        for points in self.fitness_lines:
            pygame.draw.aaline(self.win, (0,255,0), points[0],points[1],5 )

        # car
        #self.car.draw_shadow(self.win, (255,0,200))

        pygame.draw.polygon(self.win,(0,0,255),self.car.getVertices())#collider

        # info
        text = STAT_FONT.render("Angle: " + str(round(self.car.angle,2)) , 1, (255,255,255))
        self.win.blit(text,(self.current_w - 10 - text.get_width(), 10))
        text = STAT_FONT.render("Twirl: " + str(round(self.car.drift_angle,2)) , 1, (255,255,255))
        self.win.blit(text,(self.current_w - 10 - text.get_width(), 10 + text.get_height()))

        # vision 
        for p in self.car.get_vision(self.road):
            intersect_point = (int(p[0]), int(p[1]))
            diff = sub(intersect_point, self.car._center)
            offset_center = add(normalize(diff, scale=20), self.car._center)
            pygame.draw.aaline(self.win, (0,128,128), offset_center, intersect_point)
            
            pygame.draw.circle(self.win,(0,0,255), (int(p[0]), int(p[1])),5)
        
        pygame.display.update()
    

    def _tick(self):
        self.car.rotate_by(self.rotation)
        self.car.move()

