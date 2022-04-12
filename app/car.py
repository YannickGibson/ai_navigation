import pygame
import os
import math
CAR_IMG = pygame.image.load(os.path.join("src\\img", "car.png" ))
GHOST_IMG = pygame.image.load(os.path.join("src\\img", "ball.png" ))
IMG = GHOST_IMG
MAX_SPEED = .5

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
def norm(x):
    return math.sqrt(x[0]**2 + x[1]**2)
def normalize(x, scale):
    n = norm(x)
    return (x[0]/n * scale, x[1]/n * scale)
def lerp(a, b, p):
    return a + p*(b-a)

from enum import Enum 
RotatingState = Enum("RotatingState", "calm left right")
class Car:
    def __init__(self, x, y, angl):
        self._width = CAR_IMG.get_size()[0]/2
        self._height = CAR_IMG.get_size()[1]/2
        self._x = int(x) - self._width /2
        self._y = int(y) - self._height/2
        self.speed = 0
        self.acc = 0
        self.drift_angle = 0
        self.__angle = angl
        self._crashed = False
        self.rotating_state = RotatingState.calm

        diag_radius = math.atan(self._height/self._width) #in radians
        self._diag_sin = math.sin(diag_radius);
        self._diag_cos = math.cos(diag_radius);

        self.diagonal = norm((self._width, self._height))

        self._sight = 400
        self._center = None
        self._fit_distance = self._height  
        self._fitness_point = None

        self.x_vel = 0
        self.y_vel = 0
    @property
    def sight(self):
        return self._sight

    @property
    def center(self):
        return self._center

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
        new_rect = rotated_image.get_rect(center = IMG.get_rect(topleft = (self._x, self._y)).center)
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
        new_rect = rotated_image.get_rect(center = IMG.get_rect(topleft = (self._x, self._y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    def move(self):
        if abs(self.acc) == 1:
            if abs(self.speed) < 10:
                self.speed += self.acc * -0.8 #i say minus because i wanna flip direction
            if abs(self.speed) < 0.01:
                self.speed = 0
                return
        self.x_vel += math.cos(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc*2
        self.y_vel += math.sin(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc*2 #acc => dopredu|dozadu

        if self.drift_angle == 0: dir = 0
        elif self.drift_angle > 0: dir = 1
        else: dir = -1
        self.angle += self.drift_angle * self.speed * -0.1 * 14.5 + self.speed * -0.1 * 2.5 * dir

        self._x += self.x_vel*0.79
        self._y += self.y_vel*0.79
        self.drift_angle *= 0.967 ######
        self.x_vel *= 0.89
        self.y_vel *= 0.89
        self.speed *= 0.6

    def rotate_by(self, angl):



        if abs(self.drift_angle) < 5 - angl/5:
            pass
            #self.drift_angle += angl/5

        if angl > 1:

            self.drift_angle = lerp(self.drift_angle, 5, 0.3)
        elif angl < -1:

            self.drift_angle = lerp(self.drift_angle, -5, 0.3)
        elif angl == 0:
            self.drift_angle = lerp(self.drift_angle, 0, 0.3)
            #self.drift_angle = 0

        
    def get_vision(self, road) -> list:
        sin = math.sin(math.radians(self.angle))
        cos = math.cos(math.radians(self.angle))
        self._center = (self._x + self._diag_cos * self.diagonal,self._y + self._diag_sin * self.diagonal)
        center = self._center
        
        sin_front         = math.sin(math.radians(self.angle - 90))
        cos_front         = math.cos(math.radians(self.angle - 90))
        sin_mid_right     = math.sin(math.radians(self.angle - 45))
        cos_mid_right     = math.cos(math.radians(self.angle - 45))
        sin_mid_left      = math.sin(math.radians(self.angle + 45))
        cos_mid_left      = math.cos(math.radians(self.angle + 45))
        sin_mid_mid_right = math.sin(math.radians(self.angle - 67.5))
        cos_mid_mid_right = math.cos(math.radians(self.angle - 67.5))
        sin_mid_mid_left  = math.sin(math.radians(self.angle + 67.5))
        cos_mid_mid_left  = math.cos(math.radians(self.angle + 67.5))

        front_point = (center[0] + self._sight * cos_front, center[1] + self._sight * sin_front)
        back_point = (center[0] - self._sight * cos_front, center[1] - self._sight * sin_front)
        right_point = (center[0] + self._sight * cos, center[1] + self._sight * sin)
        left_point = (center[0] -self. _sight * cos, center[1] - self._sight*sin)
        mid_right_point = (center[0] + self._sight * cos_mid_right, center[1] + self._sight * sin_mid_right)
        mid_left_point = (center[0] - self._sight * cos_mid_left, center[1] - self._sight * sin_mid_left)
        mid_mid_right_point = (center[0] + self._sight * cos_mid_mid_right, center[1] + self._sight * sin_mid_mid_right)
        mid_mid_left_point = (center[0] - self._sight * cos_mid_mid_left, center[1] - self._sight * sin_mid_mid_left)

        vision = [front_point, right_point, back_point, left_point, mid_right_point, mid_left_point, mid_mid_right_point, mid_mid_left_point]

        for points in road:#2 sets of points...inner,outter
            for i in range(len(points)):
                for x, v in enumerate(vision):
                    intersect_point = self._cross(
                        points[i-1],
                        points[i],
                        center,
                        v
                    )
                    if intersect_point:
                        vision[x] = intersect_point


        return vision

    def vision_distance(self, road):
        vision = self.get_vision(road)
        sin_front         = math.sin(math.radians(self.angle - 90))
        cos_front         = math.cos(math.radians(self.angle - 90))

        # get point that is middle in the front of the car
        self._fitness_point = (self._center[0] +  self._fit_distance * cos_front, self._center[1] + self._fit_distance * sin_front)

        
        distances = []
        for p in vision:
            vect = sub(self._center, p)
            d = norm(vect)
            distances.append(round(d))

        return distances
    
    def getVertices(self):
        center = (self._x + self._diag_cos * self.diagonal,self._y + self._diag_sin * self.diagonal)

        vect = sub(center, (self._x, self._y) ) # vector from top left to center

        vect_tl = sub((self._x,self._y), center) # vect from center to Top Left not rotated
        vect_tr = (vect[0], -vect[1])
        vect_bl = (-vect[0], vect[1])
        vect_br = vect
        

        #current COS & SIN
        s = math.sin(math.radians(self.__angle))
        c = math.cos(math.radians(self.__angle))

        # rotate point
        new_tl = (vect_tl[0] * c - vect_tl[1] * s, vect_tl[0] * s + vect_tl[1] * c)
        new_tr = (vect_tr[0] * c - vect_tr[1] * s, vect_tr[0] * s + vect_tr[1] * c)
        new_bl = (vect_bl[0] * c - vect_bl[1] * s, vect_bl[0] * s + vect_bl[1] * c)
        new_br = (vect_br[0] * c - vect_br[1] * s, vect_br[0] * s + vect_br[1] * c)
        
        # translate point relevant to car position
        top_left = add(new_tl, center)
        top_right = add(new_tr, center)
        bottom_left = add(new_bl, center)
        bottom_right = add(new_br, center)


        return (top_left, top_right, bottom_right, bottom_left)

    def collide_fitness(self, a1, a2):
        return self._cross(a1, a2, self._center, self._fitness_point)

    def _cross(self, a1, a2, b1, b2):
        #vectA = a2 - a1
        r = a2[0] - a1[0], a2[1] - a1[1]
        s = b2[0] - b1[0], b2[1] - b1[1]

        """
        a2 = a1 + r
        a1 + t*r = b1 + u*s ... / scalar s
        (a1 x s) + t*(r x s) = (b1 x s) + u*(s x s) ... # s x s = 0
        (a1 x s) + t*(r x s) = (b1 x s) ... / (a1 x s)
        t*(r x s) = ((b1 - a1) x s) ... / (r x s)
        t = ((b1 - a1) x s) / (r x s)
        """
        t = u = None
        if scalar(r, s) != 0:
            t = scalar( sub(b1, a1)  , s) / scalar(r, s)
        if scalar(s, r) != 0:   
            u = scalar( sub(a1, b1)  , r) / scalar(s, r)

        if t is not None and 0 <= t <= 1 and u is not None and 0 <= u <= 1:
            x = a1[0] + r[0]*t
            y = a1[1] + r[1]*t
            return (x, y)
        return False


    def collides(self,road):
        vertices = self.getVertices()
        for points in road:
            for i in range(len(points)):
                for k in range(len(vertices)):
                    if self._cross(
                            points[i-1],
                            points[i],
                            vertices[k-1],
                            vertices[k]
                        ):

                        # Todo: collisions maybe
                        """ self.speed /= -0.8
                        #self.acc *= -1 we change that from outside
                        self.xVel /= -0.93
                        self.yVel /= -0.93 
                        self.x += self.xVel
                        self.y += self.yVel """
                        return True


