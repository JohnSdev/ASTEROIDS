import sys
import random
import pygame
import os
from multiprocessing import Process

from pygame.locals import *
from iot import *

from game import Game
from polygon import *
from stars import Stars
from bullet import Bullet
from shield import Shield


class Asteroids( Game ):
    """
    Asteroids extends the base class Game to provide logic for the specifics of the game
    """
    def __init__(self, name, width, height):

        super().__init__( name, width, height )

        self.lives = 3
        self.score = 0
        self.level = 1
        self.timeToNewLevel= 5
        self.timeWhenLevelEnds=time.time()
        #Create Ship
        self.ship = None
        #Lists for polygons
        self.asteroid_small=[ Point(-10,randint(3,8)), Point(-10,randint(8,12)), Point(randint(3,9),10), Point(15,4), Point(18,-10), Point(-5,-10), Point(-15,-5)]
        self.asteroid_big=[ Point(-30,randint(5,10)), Point(-20,randint(25,35)), Point(randint(15,25),30), Point(40,12), Point(38,-20), Point(-10,-30), Point(-35,-5)]
        self.explosionlist=[Point(0,0), Point(-3,3), Point(3,3)]
        self.shipexplosion= [Point(-2,0), Point(0,22), Point(3,-4)]
        #Create asteroidws
        self.createAsteroids(self.level)

        self.iot=iot() #IOT Hub object
        self.iotScoreSent=""
        
        self.gamestate="Newgame"

        #Creates stars
        self.stars=[]
        for i in range(400): #Creates stars
            starx=randint(0,width)
            stary=randint(0,height)
            self.stars.append(Stars(starx,stary,1,1,""))

        self.bullets = []
        self.explosion =[]
        self.shields =[]
        self.myfont = pygame.font.SysFont(None, 25, True)
        self.smallfont = pygame.font.SysFont(None, 15)
        self.gameoverFont = pygame.font.SysFont("monospace", 40, True)
        self.newLevelFont =pygame.font.SysFont("monospace", 50, True)
        self.startingInFont= pygame.font.SysFont("monospace",25,True)
        #Sounds
        


    def handle_input(self):
        super().handle_input()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_LEFT] and self.ship:
            self.ship.rotate(-8)
        if keys_pressed[K_RIGHT] and self.ship:
            self.ship.rotate(8)
        if keys_pressed[K_UP] and self.ship:
            self.ship.accelerate(0.35)
        if keys_pressed[K_DOWN] and self.ship:
            self.ship.accelerate(-0.35)
        if keys_pressed[K_s] and self.ship:
            self.ship.accelerate(0.000)
        if keys_pressed[K_SPACE] and self.ship: #Bullet handlder
            if self.ship.bulletLeft(self.bullets.__len__())== True:
                if self.ship.bulletOkay() ==True:
                    self.bullets.append(Bullet(self.ship.getX(),self.ship.getY(),self.ship.getRotation()))
        if keys_pressed[K_a] and self.ship:
            self.ship.teleport()
        if keys_pressed[K_d] and self.ship:
            if self.ship.shieldCount>0:
                self.shields.append(Shield(self.ship.position.x,self.ship.position.y))
                self.ship.shieldCount = self.ship.shieldCount-1
        if keys_pressed[K_e] and self.ship:
            self.asteroids.clear()

        if self.gamestate=="Newgame" or self.gamestate=="Gameover":
            if keys_pressed[K_RETURN]:
                if self.gamestate =="Gameover":
                    self.asteroids.clear()
                    self.level=1
                    self.score=0
                    self.createAsteroids(self.level)

                self.gamestate="Playing"
                self.startGame()
                

        else:
            pass


    def startGame(self):
        self.ship = Ship([ Point(0,0), Point(-15,15), Point(15,0), Point(-15,-15) ])
        self.lives=3


    def update_simulation(self):
        """
        update_simulation() causes all objects in the game to update themselves
        """
        for asteroid in self.asteroids:
            print(asteroid.pull.x)


        for smallStar in self.explosion:
            if time.time() - smallStar.created  >= 1 :
                self.explosion.remove(smallStar)

        super().update_simulation()
        
        for explosion in self.explosion:
            explosion.update( self.width, self.height )

        if self.ship:
            self.ship.update( self.width, self.height )
        for asteroid in self.asteroids:
            asteroid.update( self.width, self.height )
        for star in self.stars:
            star.update( self.width, self.height )
        for bullet in self.bullets:
            if bullet.remove(bullet):
                bullet.update()
            else:
                self.bullets.remove(bullet)
        for shield in self.shields:
            shield.update(self.width,self.height, self.ship.position.x,self.ship.position.y)


        if self.asteroids.__len__() == 0:
            self.level = self.level + 1
            self.gamestate = "BetweenLevels"
            self.createAsteroids(self.level)
            self.timeWhenLevelEnds=time.time()

            for asteroid in self.asteroids:
                asteroid.pull.x=0
                asteroid.pull.y=0

        if self.gamestate=="BetweenLevels":
            if time.time()-self.timeWhenLevelEnds>=5:
                self.gamestate="Playing"
                for asteroid in self.asteroids:
                    asteroid.accelerate(self.level)
            self.timeToNewLevel=int(time.time()-self.timeWhenLevelEnds)

            pass


        
        self.handle_collisions()
        self.handle_collisions_ship()

    def render_objects(self): #Obj plus text rendering
        """
        render_objects() causes all objects in the game to draw themselves onto the screen
        """

        super().render_objects()
        for exp in self.explosion:
                exp.draw( self.screen)
        # Render the ship:
        if self.gamestate==True:
            pass
        if self.ship:
            if time.time()-self.ship.respawntime < 3:
                if self.ship.color==(127,255,0):
                    self.ship.color=self.ship.switchColor
                else:
                    self.ship.color=(127,255,0)
            else:
                #fixAR SÅ ALLTID RÄTT FÄRG
                self.ship.color=(127,255,0)
            self.ship.draw( self.screen )
        # Render all the stars, if any:
        for star in self.stars:
            star.draw( self.screen )
        # Render all the asteroids, if any:
        for asteroid in self.asteroids:
            asteroid.draw( self.screen )
        # Render all the bullet, if any:
        for bullet in self.bullets:
            bullet.draw( self.screen )

        for shield in self.shields:
            shield.draw(self.screen)

        #Text to render
        self.textRendering()
        

    def textRendering(self):
        lives = self.myfont.render("Lives: {}".format(str(self.lives)), 1, (255,255,0))
        newgame=self.gameoverFont.render("Star Wars", 1, (255,255,0))
        gameover=self.gameoverFont.render("GAME OVER", 1, (255,255,0))
        gameover_info=self.myfont.render("Press ENTER to start a new game", 1, (255,255,0))
        helpKeys=self.myfont.render("SPACE = Shoot, S = Brake, D = Shield, ARROWKEYS = Fly ", 1, (255,255,0))
        score=self.myfont.render("Score: {}".format(str(self.score)), 1, (255,255,0))
        ammo = self.myfont.render("Ammo: {}".format(str((self.bullets.__len__()-5)*-1)), 1, (255,255,0))
        iotconnection=self.smallfont.render("Connected to IOT Hub", 1, (255,255,0))
        iotscore=self.myfont.render("HighScore sent to IOT Hub", 1, (255,255,0))
        level = self.myfont.render("Level: {}".format(str(self.level)),1,(255,255,0))
        file =  open("highscore.txt", "r")
        highscorefile= file.read()
        newLevel = self.newLevelFont.render("LEVEL: {}".format(str(self.level)),1,(255,255,0))
        startingIn =self.startingInFont.render("Starting in...{}".format(str((self.timeToNewLevel-5)*-1)),1,(255,255,0))
        highscore = self.myfont.render("highscore: {}".format(highscorefile),1,(255,255,0))

        file.close()
        self.screen.blit(lives, (self.width-130, self.height-580))
        self.screen.blit(score, (self.width-770, self.height-580))
        self.screen.blit(ammo, (self.width-130, self.height-550))
        self.screen.blit(highscore, (self.width-770, self.height-550))
        self.screen.blit(level,(self.width-130,self.height-520))


        if self.gamestate=="Gameover":
            self.screen.blit(gameover, (285, 200))
            self.screen.blit(gameover_info, (250, 260))
            self.screen.blit(iotscore, (275, 100))
            self.instructions()

        elif self.gamestate=="Newgame":
            self.screen.blit(newgame, (290, 200))
            self.screen.blit(gameover_info, (250, 260))
            self.screen.blit(helpKeys, (140, 300))
            self.instructions()
        elif self.gamestate=="BetweenLevels":
            self.screen.blit(newLevel, (290,200))
            self.screen.blit(startingIn, (290,260))

        if self.iot:
            self.screen.blit(iotconnection, (self.width-770, self.height-520))

    def handle_collisions(self):
        effectastro = pygame.mixer.Sound('explo1.wav')
        destruction = pygame.mixer.Sound('explo.wav')
        if self.gamestate=="BetweenLevels":
            pass
        else:
            for b in self.asteroids:
                if self.bullets.__len__()>0:
                    for i in self.bullets:
                        if b.contains(i.position) and b.small==False:
                                #Creates 3 new smaller asteroids and removes the bigger one
                                effectastro.play()
                                self.bullets.remove(i)
                                self.asteroids.append(Asteroid_s(self.asteroid_small, b.position.x, b.position.y, 0))
                                self.asteroids.append(Asteroid_s(self.asteroid_small, b.position.x, b.position.y, 180))
                                self.asteroids.append(Asteroid_s(self.asteroid_small, b.position.x, b.position.y, 250))
                                self.asteroids.remove(b)
                                self.score+=500
                        elif b.contains(i.position):
                                #kills small asteroid and creates debris
                                effectastro.play()
                                self.bullets.remove(i)
                                self.asteroids.remove(b)
                                self.explosions(b.position.x,b.position.y)
                                self.score+=200
                elif self.gamestate=="Gameover":
                    pass




    def handle_collisions_ship(self):
        destruction = pygame.mixer.Sound('explo.wav')
        for a in self.asteroids:
            if self.gamestate=="Playing" and (time.time() - self.ship.respawntime) > 3:
                if self.ship.collide(a):
                    destruction.play()
                    self.crash(a)

    
    def explosions(self,x,y):
        self.explosion.append(Asteroid_s(self.explosionlist,x, y, 20))
        self.explosion.append(Asteroid_s(self.explosionlist,x, y,120))
        self.explosion.append(Asteroid_s(self.explosionlist,x, y, 240))
                 

        

    def instructions(self):
        help
    def crash(self,asteroid121):
        if self.shields.__len__()>0:
          self.shields.clear()
          self.asteroids.remove(asteroid121)

        else:
            print("Lives:{}".format(self.lives))
            print("Ship destroyed")
            self.explosion.append((Asteroid_s(self.shipexplosion, self.ship.position.x, self.ship.position.y, 0)))
            self.explosion.append((Asteroid_s(self.shipexplosion, self.ship.position.x, self.ship.position.y, 120)))
            self.explosion.append((Asteroid_s(self.shipexplosion, self.ship.position.x, self.ship.position.y, 240)))
            
            self.ship.position=Point(400,300) 
            self.ship.respawntime=time.time()
            self.ship.pull=Point(0,0)
            self.lives = self.lives - 1
            
            

            if self.lives < 0: ## Gör Gameover funktion istället
                self.gameOver()


        

    def gameOver(self):
        hsfile = open('highscore.txt', 'r')
        hs = int(hsfile.read())
        hsfile.close()
        self.iot.iothub_client_telemetry_sample_run(self.score) #Send score to Azure IOT Hub 
                    
        if self.score > hs:
            hsfile1= open('highscore.txt', 'w' )
            hsfile1.write(str(self.score))
        self.gamestate="Gameover"

        self.ship=None
        self.lives="-"

    def createAsteroids(self,level):
        levelRange =int(level/2+9)
        self.asteroids = [Asteroid(self.asteroid_big) for i in range(levelRange)]
        for asteroid in self.asteroids:
            if self.level > 1 and self.level<10:
                asteroid.accelerate(self.level)

            else:
                asteroid.resetSpeed()

        