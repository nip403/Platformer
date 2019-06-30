from Levels import *
import pygame

#add skins
class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.velx = 0
        self.vely = 0
        self.accx = 0
        self.accy = 0

        self.gravity = 1
        self.friction = 0.5
        self.mass = 1

        self.width = 50
        self.height = 100

        self._update_rect()
        self.can_jump = True

    def draw(self,surf):
        pygame.draw.rect(surf,(0,0,0),pygame.Rect(self.x,self.y,self.width,self.height),0)

    def _update_rect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def update(self,objects):
        if abs(self.velx) < self.friction:
            self.velx = 0
        else:
            self.velx -= self.friction if self.velx > 0 else -self.friction

        if abs(self.vely) < self.friction:
            self.vely = 0
        else:
            self.vely -= self.friction if self.vely > 0 else -self.friction

        self.velx += self.accx
        self.vely += self.accy
        self.vely += self.gravity
        
        self.x += self.velx
        self.y += self.vely

        rects = [pygame.Rect(*list(map(int,o[2:6]))) if o[1] == "Rect" else pygame.Rect(int(o[2])-int(o[4]),int(o[3])-int(o[4]),int(o[4])*2,int(o[4])*2) for o in objects]
        self._update_rect()

        for r in rects:
            if self.rect.colliderect(r):
                self.can_jump = True

                if self.rect.bottom > r.top:
                    self.y = r.top - self.height
                    self.vely = 0 if self.vely > 0 else self.vely
                    self.accy = 0 if self.accy > 0 else self.accy

                elif self.rect.left < r.right:
                    self.x = r.right
                    self.velx = 0 if self.velx < 0 else self.velx
                    self.accx = 0 if self.accx < 0 else self.accx

                elif self.rect.right > r.left:
                    self.x = r.left - self.width
                    self.velx = 0 if self.velx > 0 else self.velx
                    self.accx = 0 if self.accx > 0 else self.accx

class Game:
    def __init__(self,player,details):
        self.player = player
        self.surf = details.surf
        self.clock = details.clock
        self.size = details.size
        self.details = details

        # load level 0 (tutorial)
        self.level_manager = Level(self.player,0)

    def run(self):
        self.level_manager.load()
        inst = GameInstance(self.player,self.level_manager,self.details)
        inst.run()
