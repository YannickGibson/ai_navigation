import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from abc import abstractmethod
from car import Car, add, sub, normalize
import pickle
import math
import pygame


#WIN_WIDTH = 1540
#WIN_HEIGHT = 750
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
class Simulation:
    FRAMERATE = 60
    MAX_FRAMES_PASSED = 250
    def _load_road(self):
        # load road
        with open(f"src/pickles/roads/road{self.road_index}.pickle","rb") as f:
            self.road = pickle.load(f)

    def _load_fitness(self):
        # load fitness lines
        with open(f"src/pickles/fitness/fitnessLines{self.road_index}.pickle","rb") as f:
            self.fitness_lines = pickle.load(f)
            
    def __init__(self, road_index):
        self.road_index = road_index
        self.rotation = 0
        self.run_flag = False
        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30) # gives us the top bar

        self.current_w, self.current_h = pygame.display.Info().current_w, pygame.display.Info().current_h

        self._load_fitness()
        self._load_road()

        self._set_spawn()
        self.car = Car(*self.spawn_point, self.spawn_deg)

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

class TestSimulation(Simulation):
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
        text = STAT_FONT.render("drift_angle: " + str(round(self.car.drift_angle,2)) , 1, (255,255,255))
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








import neat
import time
import pickle

class ExitSimulationException(BaseException):
    pass

class AiSimulation(Simulation):
    def __init__(self, 
            road_index = 0,
            show_active_fitness_lines = True,
            show_car_vision = False,
            show_all_fitness_lines = False,
            show_parent = True,
            save_best_genome = False,
            reverse_fitness_lines = False,
            ):
        self.show_active_fitness_lines = show_active_fitness_lines
        self.show_car_vision = show_car_vision
        self.show_all_fitness_lines = show_all_fitness_lines
        self.show_parent = show_parent
        self.save_best_genome = save_best_genome
        self.gen_num = 0
        self.rotation = 0;
        self.champion_not_beaten_n = 0
        self.population = None
        self.prev_best_genome = None
        self.reverse_fitness_lines = reverse_fitness_lines


        super().__init__(road_index)

    def _load_fitness(self):
        super()._load_fitness()
        if self.reverse_fitness_lines:
            self.fitness_lines = list(reversed(self.fitness_lines))

    def _draw(self):

        if self.car.collides(self.road):
            self.win.fill((200,50,50))
        else:
            self.win.fill((0,0,0))
        
        #road
        pygame.draw.polygon(self.win, (140,124,215), [self.road[1][0],self.road[0][0]] + self.road[0] + self.road[1])

        #cars
        best_genome_car = None
        for i, car in enumerate(self.cars):
            
            if self.show_active_fitness_lines:
                #fitness lines for each car
                pygame.draw.line(self.win,(0,255,255),self.fitness_lines[ self.fit_indexes[i] ][0], self.fitness_lines[ self.fit_indexes[i] ][1],2)

                pygame.draw.line(self.win,(255,0,0),self.fitness_lines[ self.fit_indexes[i]-4 ][0], self.fitness_lines[ self.fit_indexes[i]-4 ][1])

            if self.show_car_vision:
                for p in car.get_vision(self.road):
                    pygame.draw.aaline(self.win, (255,0,255),car.center, (int(p[0]),int(p[1])),1)
                    pygame.draw.circle(self.win,(0,25,255),(int(p[0]),int(p[1])),3) 
                    
            if self.show_parent and self.population.best_genome == self.ge[i]:
                best_genome_car = car
            else:
                car.draw(self.win)
            

        self.car.draw_shadow(self.win,(0,0,255))

        #info
        text = STAT_FONT.render("Car count: " + str(len(self.cars)) , 1, (255,255,255))
        self.win.blit(text,(self.current_w - 10 - text.get_width(), 10))
        text = STAT_FONT.render("Frames passed: {}".format(self.frames_passed), 1, (255,255,255))
        self.win.blit(text,(self.current_w - 10 - text.get_width(), text.get_height() + 20))
        text = STAT_FONT.render("Gen: " + str(self.gen_num), 1, (255,255,255))
        self.win.blit(text,(10, 10))

        if self.show_all_fitness_lines:
            #fitness lines
            pygame.draw.line(self.win, (255,0,0), self.fitness_lines[0][0],self.fitness_lines[0][1],5 )
            for points in self.fitness_lines[1:]:
                pygame.draw.line(self.win, (255,255,0), points[0],points[1],5 )
                
        if best_genome_car is not None:
            best_genome_car.draw_shadow(self.win,(255,128,128))

        pygame.display.update()

    def _iterate_ai(self, genomes, config):
        self.gen_num += 1
        self.frames_passed = 0

        if self.population.best_genome != None and self.population.best_genome == self.prev_best_genome:
            self.champion_not_beaten_n += 1
            print("[{}]: Best genome not beaten: {} times".format(time.strftime("%H:%M %Ss"), self.champion_not_beaten_n))
        else:
            self.champion_not_beaten_n = 0
            self.prev_best_genome = self.population.best_genome
            print("[{}]: New best genome leads the race".format(time.strftime("%H:%M %Ss")))

        

        self.nets = []
        self.ge = []
        self.cars = []

        for _ ,g in genomes: # (id, obj)
            net = neat.nn.FeedForwardNetwork.create(g, config) # input, output
            self.nets.append(net)
            c = Car(*self.spawn_point, self.spawn_deg)
            self.cars.append(c)
            g.fitness = 0
            self.ge.append(g)
        
        self.fit_indexes = [0 for _ in self.cars] # index of last fitnessLine they crossed

        if super().run(): 
            raise ExitSimulationException()



    def _register_keys(self, event):
        if super()._register_keys(event): return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                print("[{}]: Skipping generation {}".format(time.strftime("%H:%M %Ss"), self.gen_num))
                self.run_flag = False
                return True

        return False


    def _think(self, car: Car, i: int):
        # input -> get output from net
        
        # input: [f_dist, r_dist, b_dist, l_dist, mr_dist, ml_dist, mmr_dist. mml_dist] [drift_angle, speed]
        vision = car.vision_distance(self.road)
        for _i in range(len(vision)):
            vision[_i] = vision[_i]/car.sight

        front_acc, back_acc, rot = self.nets[i].activate(vision + [car.drift_angle/360, car.speed]) #drifitng
        if rot > .4: car.rotate_by(5)
        elif rot < -.6: car.rotate_by(-5)
        else: car.rotate_by(0)

        if front_acc > 0.3: car.acc = 1
        elif back_acc > 0.3: car.acc = -1
        else:  car.acc = 0

        car.move()
        
        front_line = self.fitness_lines[self.fit_indexes[i]] # check if crossing fitness_lines in direction of the race
        back_line = self.fitness_lines[ self.fit_indexes[i] - 4 ] # check if going back
        if car.collide_fitness(front_line[0], front_line[1]):
            self.ge[i].fitness += 0.1
            pygame.draw.line(self.win,(255,0,250), *front_line,10)
            self.fit_indexes[i] += 1
        elif car.collide_fitness(back_line[0], back_line[1]):
            self.ge[i].fitness -= 0.5
            self.fit_indexes[i] -= 1

        self.fit_indexes[i] %= len(self.fitness_lines) # put it back to the world of Zn

    def _tick(self):

        self.car.rotate_by(self.rotation) 
        self.car.move()
        for i, car in enumerate(self.cars):

            if car.collides(self.road):
                del self.cars[i]
                del self.nets[i]
                del self.ge[i]
                del self.fit_indexes[i]
                continue
                    
            self._think(car, i)

        if len(self.cars) <= 0 or self.frames_passed > Simulation.MAX_FRAMES_PASSED:
            return True

        self.frames_passed += 1
        return False

    def run(self):
        self.win = pygame.display.set_mode((self.current_w, self.current_h))

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "../src/config-feedforward.txt")

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path)
        p = neat.Population(config)
        self.population = p

        #showing stats
        #p.add_reporter(neat.StdOutReporter())
        #p.add_reporter(neat.StatisticsReporter())

        try:
            best_genome = p.run(self._iterate_ai, n=10000)# num of generations
        except ExitSimulationException:
            pass
        if self.save_best_genome: self.save_genome(best_genome)
        return False

    def save_genome(genome):
        i = 0
        while os.path.exists("src/pickles/genomes_drift/dgenome{}.pickle".format(i)):
            i += 1
        
        with open("src/pickles/genomes_drift/dgenome{}.pickle".format(i), "wb") as f:
            pickle.dump(genome, f)
            print("Genome pickle saved")


