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
        self.width = CAR_IMG.get_size()[0]/2
        self.height = CAR_IMG.get_size()[1]/2
        self.x = int(x) - self.width /2
        self.y = int(y) - self.height/2
        self.speed = 0
        self.acc = 0
        self.__angle = angl
        self.driftAngle = 0
        self.crashed = False

        diagRadius = math.atan(self.height/self.width) #in radians
        self.diagSin = math.sin(diagRadius);
        self.diagCos = math.cos(diagRadius);

        self.radius = math.sqrt(self.width*self.width + self.height*self.height)

        self.sight = 400
        self.center = None

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
        #current COS & SIN
        sin = math.sin(math.radians(self.angle))
        cos = math.cos(math.radians(self.angle))
        self.center = (self.x + self.diagCos * self.radius,self.y + self.diagSin * self.radius)
        center = self.center
        
        sinFront = math.sin(math.radians(self.angle - 90))
        cosFront = math.cos(math.radians(self.angle - 90))
        sinMidRight = math.sin(math.radians(self.angle - 45))
        cosMidRight = math.cos(math.radians(self.angle - 45))
        sinMidLeft = math.sin(math.radians(self.angle + 45))
        cosMidLeft = math.cos(math.radians(self.angle + 45))
        sinMidMidRight = math.sin(math.radians(self.angle - 67.5))
        cosMidMidRight = math.cos(math.radians(self.angle - 67.5))
        sinMidMidLeft = math.sin(math.radians(self.angle + 67.5))
        cosMidMidLeft = math.cos(math.radians(self.angle + 67.5))

        frontPoint = (center[0] + self.sight * cosFront, center[1] + self.sight * sinFront)
        backPoint = (center[0] - self.sight * cosFront, center[1] - self.sight * sinFront)
        rightPoint = (center[0] + self.sight * cos, center[1] + self.sight * sin)
        leftPoint = (center[0] -self. sight * cos, center[1] - self.sight*sin)
        midRightPoint = (center[0] + self.sight * cosMidRight, center[1] + self.sight * sinMidRight)
        midLeftPoint = (center[0] - self.sight * cosMidLeft, center[1] - self.sight * sinMidLeft)
        midMidRightPoint = (center[0] + self.sight * cosMidMidRight, center[1] + self.sight * sinMidMidRight)
        midMidLeftPoint = (center[0] - self.sight * cosMidMidLeft, center[1] - self.sight * sinMidMidLeft)

        vision = [frontPoint, rightPoint, backPoint, leftPoint, midRightPoint, midLeftPoint, midMidRightPoint, midMidLeftPoint]

        for points in road:#2 sets of points...inner,outter
            for i in range(len(points)):
                for x, v in enumerate(vision):
                    intersect = self.cross(
                        points[i-1],
                        points[i],
                        center,
                        v
                    )
                    if intersect:
                        vision[x] = intersect


        return vision
    def visionDistance(self, road):
        pass
    
    def getVertices(self):
        center = (self.x + self.diagCos * self.radius,self.y + self.diagSin * self.radius)

        vect = sub(center, (self.x, self.y) ) # vector from top left to center

        vectTL = sub((self.x,self.y), center) # vect from center to Top Left not rotated
        vectTR = (vect[0], -vect[1])
        vectBR = vect
        vectBL = (-vect[0], vect[1])
        

        #current COS & SIN
        s = math.sin(math.radians(self.__angle))
        c = math.cos(math.radians(self.__angle))

        # rotate point
        newTL = (vectTL[0] * c - vectTL[1] * s, vectTL[0] * s + vectTL[1] * c)
        newTR = (vectTR[0] * c - vectTR[1] * s, vectTR[0] * s + vectTR[1] * c)
        newBR = (vectBR[0] * c - vectBR[1] * s, vectBR[0] * s + vectBR[1] * c)
        newBL = (vectBL[0] * c - vectBL[1] * s, vectBL[0] * s + vectBL[1] * c)
        
        # translate point relevant to car position
        topLeft = add(newTL, center)
        topRight = add(newTR, center)
        bottomLeft = add(newBL, center)
        bottomRight = add(newBR, center)


        return (topLeft, topRight, bottomRight, bottomLeft)


    def cross(self, a1, a2, b1, b2):
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
                    if self.cross(
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


