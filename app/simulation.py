from abc import abstractmethod
import pygame
import os
from carDrift import Car, add, sub
import pickle
import math


WIN_WIDTH = 1540
WIN_HEIGHT = 750
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
class Simulation:
    def load_road(self):
        # load road
        with open(f"src/pickles/roads/road{self.road_index}.pickle","rb") as f:
            self.road = pickle.load(f)

    def load_fitness(self):
        # load fitness lines
        with open(f"src/pickles/fitness/fitnessLines{self.road_index}.pickle","rb") as f:
            self.fitnessLines = pickle.load(f)
            print("src/pickles/fitness/fitnessLines loaded")
    def __init__(self):
        self.road_index = 0
        self.rotation = 0
        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

        #self.current_w, self.current_h = pygame.display.Info()["current_w"], pygame.display.Info()["current_h"]

        self.load_fitness()
        self.load_road()

        self.set_spawn()
        self.car = Car(*self.spawn_point, self.spawn_deg)

    def set_spawn(self):
        diff1 = sub(*self.fitnessLines[0])
        diff2 = sub(*self.fitnessLines[-1])
        c1 = sub(self.fitnessLines[0][0], (diff1[0]/2, diff1[1]/2)) # center of first fit line
        c2 = sub(self.fitnessLines[-1][0], (diff2[0]/2, diff2[1]/2)) # center of last fit line
        diff3 = sub(c1, c2)
        spawnPoint = sub(c1, (diff3[0]/2, diff3[1]/2)) # middle of the two center

        self.spawn_point = (int(spawnPoint[0]), int(spawnPoint[1])) 

        spawnRadians = math.atan2(c2[1]-c1[1], c2[0]-c1[0])
        self.spawn_deg = math.degrees(spawnRadians) - 90

    def register_keys(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

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

        return True
    def run(self):
    
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()
        while True:
            clock.tick(120)
            for event in pygame.event.get():
                if (not self.register_keys(event)):
                    return 
                    
            self.tick() # implement this
            
            self.draw()
    @abstractmethod
    def draw():
        ...
    @abstractmethod
    def tick():
        ...

class TestSimulation(Simulation):
    def __init__(self):
        super().__init__()
    def draw(self):
        #background
        if self.car.collides(self.road):
            self.win.fill((255,0,0))
        else:
            self.win.fill((0,0,0))
        
        # road
        pygame.draw.polygon(self.win, (255,255,255), self.road[0] + self.road[1])
        
        #fitness lines
        for points in self.fitnessLines:
            pygame.draw.aaline(self.win, (0,255,0), points[0],points[1],5 )

        # car
        self.car.draw_shadow(self.win, (255,0,200))

        #pygame.draw.polygon(self.win,(0,0,255),self.car.getVertices())#collider

        # info
        text = STAT_FONT.render("Angle: " + str(round(self.car.angle,2)) , 1, (255,255,255))
        self.win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10))
        text = STAT_FONT.render("DriftAngle: " + str(round(self.car.driftAngle,2)) , 1, (255,255,255))
        self.win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10 + text.get_height()))

        # vision 
        for p in self.car.visionPoints(self.road):
            intersect_point = (int(p[0]), int(p[1]))
            diff = sub(intersect_point, self.car.center)
            offset_center = add(normalize(diff, scale=20), self.car.center)
            pygame.draw.aaline(self.win, (0,128,128), offset_center, intersect_point)
            
            pygame.draw.circle(self.win,(0,0,255), (int(p[0]), int(p[1])),5)
        
        pygame.display.update()
    

    def tick(self):
        self.car.rotateBy(self.rotation)
        self.car.move()

    def register_keys(self, event):
        return super().register_keys(event)

def norm(x):
    return math.sqrt(x[0]**2 + x[1]**2)
def normalize(x, scale):
    n = norm(x)
    return (x[0]/n * scale, x[1]/n * scale)