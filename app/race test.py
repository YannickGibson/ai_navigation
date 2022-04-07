import pygame
import os
from carDrift import Car, add, sub
import pickle
import neat
import math
pygame.font.init()

pygame.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
screen_width,screen_height = info.current_w,info.current_h
#These are the dimensions of your screen/monitor. You can use these or reduce them to exclude borders and title bar:

WIN_WIDTH = 1540
WIN_HEIGHT = 750


def draw(win, car, road, fitnessLines):
    #background
    if car.collides(road):
        win.fill((255,0,0))
    else:
        win.fill((0,0,0))
    
    # road
    pygame.draw.polygon(win, (255,255,255), road[0] + road[1])
    
    #fitness lines
    for points in fitnessLines:
        if(len (points)>1):
            pygame.draw.line(win, (0,255,0), points[0],points[1],5 )
        else:
            pygame.draw.line(win, (0,255,0), points[0],pygame.mouse.get_pos(),5 )

    # car
    car.draw_shadow(win, (255,0,200))

    #pygame.draw.polygon(win,(0,0,255),car.getVertices())#collider

    # info
    text = STAT_FONT.render("Angle: " + str(round(car.angle,2)) , 1, (255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render("DriftAngle: " + str(round(car.driftAngle,2)) , 1, (255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 10 + text.get_height()))

    # vision 
    for p in car.visionPoints(road):
        intersect_point = (int(p[0]), int(p[1]))
        diff = sub(intersect_point, car.center)
        offset_center = add((diff[0]/8, diff[1]/8), car.center);
        pygame.draw.line(win, (255,0,255), offset_center, intersect_point,5)
        
        pygame.draw.circle(win,(0,0,255), (int(p[0]), int(p[1])),5)
    
    pygame.display.update()

def main():
    # load road
    with open("src/pickles/roads/road0.pickle","rb") as f:
        road = pickle.load(f)

    # load fitness lines
    with open("src/pickles/fitness/fitnessLines0.pickle","rb") as f:
        fitnessLines = pickle.load(f)
        print("src/pickles/fitness/fitnessLines loaded")
   
    c1 = add(*fitnessLines[0])
    c2 = add(*fitnessLines[-1])
    spawnPoint = add(c1, c2)
    spawn_point = (int(spawnPoint[0]/4), int(spawnPoint[1]/4)) 

    spawnRadians = math.atan2(c2[1]-c1[1], c2[0]-c1[0])
    spawn_deg = math.degrees(spawnRadians) - 90
    rotate = 0
    car = Car(*spawn_point, spawn_deg)


    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    #pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    rotate = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                #exit - wasnt working for F5 starts
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    rotate = 0
                elif event.key == pygame.K_d:
                    rotate = 0
                elif event.key == pygame.K_w:
                    car.acc = 0
                elif event.key == pygame.K_s:
                    car.acc = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    rotate = -5
                elif event.key == pygame.K_d:
                    rotate = 5
                elif event.key == pygame.K_w:
                    car.acc = 1
                elif event.key == pygame.K_s:
                    car.acc = -1
        if rotate != 0:
            car.rotateBy(rotate)

        car.move()
        draw(win, car, road, fitnessLines)



if __name__ == "__main__":
    main()

