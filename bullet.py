from circle import Circle
import pygame
from point import Point
from random import randint
from polygon import Ship

class Bullet(Circle):
    def __init__(self,x,y,rotation,r=5):
        super().__init__(x,y,r,rotation)
        self.linewidth = 0
        self.accelerate(10)
        
    def draw(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y) )
        pygame.draw.circle( screen,  (255,0,0), pos, self.radius, self.linewidth )

    def update(self, width =800, height=600):

        self.position += self.pull
        self.rotation += self.angular_velocity

        self.position.x %= width
        self.position.y %= height
        self.rotation %= 360
    def remove(self,thisBullet ,width = 800, height=600):
        if thisBullet.position.x >= width-10 or thisBullet.position.y >= height-10 or thisBullet.position.x <= 0+10 or thisBullet.position.y <= 0+10 :#fixat
            return False
        else:
            return True




