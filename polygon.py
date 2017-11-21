import math, copy
import pygame
from random import *
import time
from shape import Shape
from point import Point



class Polygon(Shape):
    def __init__(self, points=[], x=0, y=0, rotation=0):
        """ points = all coordinates for the lines in the polygon
            x, y   = the 2-dimensional coordinates for the location of the polygon
            rotation = how many degrees the polygon should be rotated
            """
        super().__init__( x, y, rotation )
        # Make our own copy of all the points that make up this polygon
        self.points = list(points)


    def draw(self, screen):
        # Since polygons can be rotated, we need to "translate" all the points
        # by the amount of rotation before we draw them:
        points = self.getRotatedPoints()
        # Convert our point objects into a list of tuples that PyGame expects:
        vectors=[]
        for p in points:
            vectors.append( (p.x, p.y) )
        pygame.draw.polygon( screen, self.color, vectors, 1 )


    def getRotatedPoints(self):
        """
        getRotatedPoints() takes all points in self.points and transforms them
        mathematically by a given rotation angle (self.rotation)
        :return: returns a new list of points that are rotated
        """
        rotated_points=copy.deepcopy(self.points)
        center = self.findCenter()
        for i in range(len(rotated_points)):
            p = rotated_points[i]
            x = ( (p.x-center.x) * math.cos( math.radians(self.rotation)) ) \
                - ( (p.y-center.y) * math.sin( math.radians(self.rotation)) ) \
                + center.x/2.0 + self.position.x
            y = ( (p.x-center.x) * math.sin( math.radians(self.rotation))) \
                + ((p.y-center.y) * math.cos( math.radians(self.rotation))) \
                + center.y/2.0 + self.position.y
            rotated_points[i].x = x
            rotated_points[i].y = y
        return rotated_points


    def findArea(self):
        """
        Compute the area of the polygon using some fun mathematics.
        This could be useful for advanced colission detection.
        :return: estimate of the area of the polygon
        """
        sum = 0
        i = 0
        j = 1
        while i < len(self.points):
            sum += (self.points[i].x * self.points[j].y) - (self.points[j].x * self.points[i].y )
            i+=1
            j=(j+1)%len(self.points)

        return math.fabs( sum/2 )


    def findCenter(self):
        """
        Computes the center point of the polygon - helps us rotate polygons more nicely
        Just ignore the maths :)
        :return: a Point (x,y) representing the "center of gravity" of the polygon
        """
        sum = Point(0,0)
        i = 0
        j = 1
        while i < len(self.points):
            sum.x +=  (self.points[i].x + self.points[j].x ) \
                        * ( self.points[i].x * self.points[j].y - self.points[j].x * self.points[i].y )
            sum.y +=  (self.points[i].y + self.points[j].y ) \
                        * ( self.points[i].x * self.points[j].y - self.points[j].x * self.points[i].y )
            i+=1
            j=(j+1)%len(self.points)
        area = self.findArea()
        return Point( math.fabs( sum.x/(6*area)), math.fabs( sum.y/(6*area)) )


    def contains(self, point):
        """
        contains()  - used for collission detection. Computes if a given Point is inside
        or outside of the polygon.
        :param point: Which point
        :return: True or False depending on if the point is inside or not
        """
        crossingNumber = 0.0
        i = 0
        j = 1
        points = self.getRotatedPoints()
        while i < len(points):
            if ( ( ( ( points[i].x < point.x ) and ( point.x <= points[j].x ) ) or
                   ( ( points[j].x < point.x ) and ( point.x <= points[i].x ) ) ) and
                 ( point.y > points[i].y + ( points[j].y - points[i].y ) / ( points[j].x - points[i].x ) * ( point.x - points[i].x ) )
               ):
                crossingNumber+=1
            i+=1
            j=(j+1)%len(self.points)

        return crossingNumber % 2 == 1


    def collide(self, poly):
        """
        We override collide() to test if two polygons overlapp each other or not
        This can be used to test e.g. if an astroid and a ship have collided
        Or if two asteroids have collided.
        :param poly: Another object of typ Polygon
        :return: True or False depending on if the two objects intersect or not.
        """
        points = poly.getRotatedPoints()

        for p in points:
            if self.contains( p ):
                return True
        return False

class Ship(Polygon):
    def __init__(self, points=[], x=395, y=295, rotation=0):
        super().__init__(points, x, y, rotation)
        self.lives=2
        self.last_shot= time.time()
        self.ammo= 4
        self.max_ammo =4
        self.color=(127,255,0)
        self.switchColor=(255,0,0)
        self.shieldCount=1
        self.respawntime=time.time()

    def bulletLeft(self,bulletListLength):
        print(bulletListLength)
        if bulletListLength > self.ammo:
            return False
        else:
            return True

    def teleport(self):
        self.position.x = randint(0,800)
        self.position.y = randint(0,600)

    def bulletOkay(self):

        self.shot_delay = 0.2
        print(time.time()- self.last_shot > self.shot_delay)
        if time.time()- self.last_shot > self.shot_delay:
            self.last_shot = time.time()
            return True
        else:
            return False

    def getX(self):
        return self.position.x
    def getY(self):
        return self.position.y
    def getRotation(self):
        return self.rotation


class Asteroid(Polygon): #Big asteroids
    def __init__(self, points=[],x=0, y=0, rotation=0, flag=""):

        self.small=False
        self.rotate=3
        rotation = randint(0,360)
        if flag == "small":
            super().__init__(points,x,y,rotation)
        else:
            xr=randint(0,800)
            yr=randint(0,600)
            super().__init__(points,xr,yr,rotation)
        self.angular_velocity=3
        self.accelerate(1)
        self.color=(0,190,190)

    def resetSpeed(self):
        self.pull.x *= 0.9
        self.pull.y *= 0.9

class Asteroid_s(Polygon): #Small asteroids
    def __init__(self, points=[],x=0, y=0, rotation=0):
        
        
        self.small=True
        self.pull = Point(3,50) 
        self.rotate=5 
        rotation = randint(0,360)
        self.created =time.time()
        self.color=(135,206,250)	

        super().__init__(points,x,y,rotation)
        self.angular_velocity=4
        self.accelerate(1.3)


        
            