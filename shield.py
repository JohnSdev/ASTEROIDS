from circle import Circle
import pygame
class Shield(Circle):
    def __init__(self,x,y,rotation=5,r=30):
        super().__init__(x,y,r,rotation)
        self.linewidth = 1
        self.accelerate=0

    def draw(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y) )
        pygame.draw.circle( screen,  (255,255,255), pos, self.radius, self.linewidth )

    def update(self, width =800, height=600,xpos=0,ypos=0):

        self.position.x=xpos
        self.position.y=ypos

        self.position.x %= width
        self.position.y %= height
        self.rotation %= 360
    def remove(self,thisBullet ,width = 800, height=600):
        pass