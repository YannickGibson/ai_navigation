
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from app.src.car.car import Car
import pickle
import pygame
from app.src.simulation.base import Simulation, STAT_FONT
import neat as neat
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
            let_me_drive = False,
            max_frames_elapsed = 400,
            no_progress_frames_elapsed = 50,
            ):
        self.show_active_fitness_lines = show_active_fitness_lines
        self.show_car_vision = show_car_vision
        self.show_all_fitness_lines = show_all_fitness_lines
        self.show_parent = show_parent
        self.save_best_genome = save_best_genome
        self.gen_num = 0
        self.rotation = 0
        self.champion_not_beaten_n = 0
        self.population = None
        self.prev_best_genome = None
        self.reverse_fitness_lines = reverse_fitness_lines
        self.let_me_drive = let_me_drive
        self.max_frames_elapsed = max_frames_elapsed
        self.no_progress_frames_elapsed = no_progress_frames_elapsed

        self.no_fitness_crossed_for = 0
        self.fitness_crossed = False

        super().__init__(road_index, self.let_me_drive)

    def _load_fitness(self):
        super()._load_fitness()
        if self.reverse_fitness_lines:
            self.fitness_lines = list(reversed(self.fitness_lines))

    def _draw(self):

        if self.let_me_drive == True and self.car.collides(self.road):
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
                    pygame.draw.aaline(self.win, (255,0,255), car.center, (int(p[0]),int(p[1])),1)
                    pygame.draw.circle(self.win,(0,25,255),(int(p[0]),int(p[1])),3) 
                    
            if self.show_parent and self.population.best_genome == self.ge[i]:
                best_genome_car = car
            else:
                car.draw(self.win)
            

        if self.let_me_drive == True: 
            if self.show_car_vision:
                for p in self.car.get_vision(self.road):
                    pygame.draw.aaline(self.win, (255,0,255), self.car.center, (int(p[0]),int(p[1])),1)
                    pygame.draw.circle(self.win,(0,25,255),(int(p[0]),int(p[1])),3) 
            self.car.draw_shadow(self.win,(0,0,255))


        #info
        text = STAT_FONT.render("Car count: " + str(len(self.cars)) , 1, (255,255,255))
        self.win.blit(text,(self.current_w - 10 - text.get_width(), 10))
        text = STAT_FONT.render("{} F".format(self.frames_passed), 1, (255,255,255))
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
            self.fitness_crossed = True
            self.ge[i].fitness += 0.1
            pygame.draw.line(self.win,(255,0,250), *front_line,10)
            self.fit_indexes[i] += 1
        elif car.collide_fitness(back_line[0], back_line[1]):
            self.ge[i].fitness -= 0.5
            self.fit_indexes[i] -= 1

        self.fit_indexes[i] %= len(self.fitness_lines) # put it back to the world of Zn

    def _tick(self):

        if self.let_me_drive == True:
            self.car.rotate_by(self.rotation) 
            self.car.move()
        self.fitness_crossed = False
        for i, car in enumerate(self.cars):

            if car.collides(self.road):
                del self.cars[i]
                del self.nets[i]
                del self.ge[i]
                del self.fit_indexes[i]
                continue
               
            self._think(car, i)

        if self.fitness_crossed:
            self.no_fitness_crossed_for = 0
        else:
            self.no_fitness_crossed_for += 1
            if self.no_fitness_crossed_for > self.no_progress_frames_elapsed:
                self.no_fitness_crossed_for = 0
                return True # new gen

        if len(self.cars) <= 0 or self.frames_passed > self.max_frames_elapsed:
            return True # new gen

        self.frames_passed += 1
        return False

    def run(self, n = 10000):
        self.win = pygame.display.set_mode((self.current_w, self.current_h))

        config_path = "app/utils/config-feedforward.txt"

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
            #self.save_best_genome
            p.run(self._iterate_ai, n=n)# num of generations
        except ExitSimulationException:
            pass
        if self.prev_best_genome: self.save_genome(self.prev_best_genome)
        return False

    def save_genome(self, genome):
        i = 0
        while os.path.exists("app\\utils\\pickles\\genomes\\genome{}.pickle".format(i)):
            i += 1
        with open("app\\utils\\pickles\\genomes\\genome{}.pickle".format(i), "wb") as f:
            pickle.dump(genome, f)
            print("Genome pickle saved")


