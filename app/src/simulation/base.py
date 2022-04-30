import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from abc import abstractmethod
from app.src.car.car import Car, sub
import pickle
import math
import pygame


#WIN_WIDTH = 1540
#WIN_HEIGHT = 750
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
class Simulation:
    FRAMERATE = 60
    def _load_road(self):
        # load road
        with open(f"app\\utils\\pickles\\roads\\road{self.road_index}.pickle","rb") as f:
            self.road = pickle.load(f)

    def _load_fitness(self):
        # load fitness lines
        with open(f"app\\utils\\pickles\\fitness\\fitnessLines{self.road_index}.pickle","rb") as f:
            self.fitness_lines = pickle.load(f)
            
    def __init__(self, road_index, let_me_drive = True):
        self.road_index = road_index
        self.let_me_drive = let_me_drive
        
        self.run_flag = False
        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30) # gives us the top bar

        self.current_w, self.current_h = pygame.display.Info().current_w, pygame.display.Info().current_h

        self._load_fitness()
        self._load_road()

        self._set_spawn()
        if self.let_me_drive:
            self.car = Car(*self.spawn_point, self.spawn_deg)
            self.rotation = 0

    def _set_spawn(self):
        diff1 = sub(*self.fitness_lines[0])
        diff2 = sub(*self.fitness_lines[-1])
        c1 = sub(self.fitness_lines[0][0], (diff1[0]/2, diff1[1]/2)) # center of first fit line
        c2 = sub(self.fitness_lines[-1][0], (diff2[0]/2, diff2[1]/2)) # center of last fit line
        diff3 = sub(c1, c2)
        spawnPoint = sub(c1, (diff3[0]/2, diff3[1]/2)) # middle of the two center

        self.spawn_point = (int(spawnPoint[0]), int(spawnPoint[1])) 

        spawnRadians = math.atan2(c2[1]-c1[1], c2[0]-c1[0])
        self.spawn_deg = math.degrees(spawnRadians) - 90

    def _register_keys(self, event) -> bool:
        if event.type == pygame.QUIT:
            self.run_flag = True
            pygame.quit()
            return True

        if self.let_me_drive == True:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.rotation = 0
                elif event.key == pygame.K_d:
                    self.rotation = 0
                elif event.key == pygame.K_w:
                    self.car.acc = 0
                elif event.key == pygame.K_s:
                    self.car.acc = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.rotation = -5
                elif event.key == pygame.K_d:
                    self.rotation = 5
                elif event.key == pygame.K_w:
                    self.car.acc = 1
                elif event.key == pygame.K_s:
                    self.car.acc = -1

        return False
    def run(self):
        self.win = pygame.display.set_mode((self.current_w, self.current_h))
        clock = pygame.time.Clock()
        while True:
            clock.tick(Simulation.FRAMERATE)
            for event in pygame.event.get():
                if (self._register_keys(event)):
                    return self.run_flag # exited correctly
                    
            if self._tick(): # implement this
                return self.run_flag # something has happened

            self._draw()
    @abstractmethod
    def _draw():
        raise NotImplementedError("Please Implement this method")
    @abstractmethod
    def _tick():
         raise NotImplementedError("Please Implement this method")
