from Levels import *
import pygame

XBOUND = 250000
YBOUND = 250000

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.velx = 0
        self.vely = 0

        self.velx_cap = 10
        self.vely_cap = 25

        self.gravity = 0.2
        self.frictionx = 0.2
        self.frictiony = 0.1
        self.mass = 1

        self.width = 25
        self.height = 50

        self.can_jump = True
        self.allow_wall_jump = False
        self.crouching = False

        self._update_rect()
        self.SpriteManager = SpriteManager(self)
        self._init_coords = [self.x,self.y]
        
    def jump(self):
        if not self.crouching:
            self.vely = -15

    def movex(self,dx):
        self.velx += dx if not self.crouching else dx/2

    def draw(self,surf):
        surf.blit(self.SpriteManager.get_sprite(),(self.details.size[0]/2 - self.width/2,self.details.size[1]/2 - self.height/2))

    def _update_rect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def update_level(self,objects):
        self.rects = [pygame.Rect(*list(map(int,o[2:6]))) if o[1] == "Rect" else pygame.Rect(int(o[2])-int(o[4]),int(o[3])-int(o[4]),int(o[4])*2,int(o[4])*2) for o in objects]

    def update(self):
        self.SpriteManager.update()

        if abs(self.velx) < self.frictionx:
            self.velx = 0
        else:
            self.velx -= self.frictionx if self.velx > 0 else -self.frictionx

        if abs(self.vely) < self.frictiony:
            self.vely = 0
        else:
            self.vely -= self.frictiony if self.vely > 0 else -self.frictiony

        if not any(self.rect.colliderect(r) and (set(range(self.x,self.x+self.width)) & set(range(r.left,r.right))) and self.rect.top < r.top for r in self.rects) and not (self.crouching and any(pygame.Rect(self.x,self.y+1,self.width,self.height).colliderect(r) for r in self.rects)):
            self.vely += self.gravity

        if self.crouching:
            if self.velx > self.velx_cap/2:
                self.velx = self.velx_cap/2
            elif self.velx < -self.velx_cap/2:
                self.velx = -self.velx_cap/2
        else:
            if self.velx > self.velx_cap:
                self.velx = self.velx_cap
            elif self.velx < -self.velx_cap:
                self.velx = -self.velx_cap

        if self.vely > self.vely_cap:
            self.vely = self.vely_cap
        elif self.vely < -self.vely_cap:
            self.vely = -self.vely_cap

        for x in range(self.x+1,int(self.x+self.velx+1)) if self.velx > 0 else reversed(range(int(self.x+self.velx),self.x)):
            self.x = x
            
            if not self.crouching:
                self._update_rect()
            else:
                self.rect = pygame.Rect(self.x,self.y+15,self.width,self.height-15)

            if any(self.rect.colliderect(r) for r in self.rects):
                self.x -= 1 if self.velx > 0 else -1
                self.velx = 0 

                if self.allow_wall_jump:
                    self.can_jump = True

                break

        for y in range(self.y+1,int(self.y+self.vely+1)) if self.vely > 0 else reversed(range(int(self.y+self.vely),self.y)):
            self.y = y

            if not self.crouching:
                self._update_rect()
            else:
                self.rect = pygame.Rect(self.x,self.y+15,self.width,self.height-15)

            if any(self.rect.colliderect(r) for r in self.rects):
                self.y -= 1 if self.vely > 0 else -1

                if self.vely < 0:
                    self.vely = 0

                if any(self.rect.colliderect(r) and self.rect.top - r.bottom < -1 for r in self.rects):
                    self.can_jump = True

                break

        if self.crouching:
            self._update_rect()

        if not -XBOUND <= self.x <= XBOUND or not -YBOUND <= self.y <= YBOUND:
            self.x,self.y = self._init_coords
            self.velx = 0
            self.vely = 0

    def crouch(self):
        self._update_rect()
        self.crouching = not self.crouching if not any(self.rect.colliderect(r) for r in self.rects) else self.crouching

class Game:
    def __init__(self,details,init_level=0):
        self.details = details
        self.level_manager = Level(0,self.details)
        self.init()

    def init(self):
        self.level_manager.load()
        self.player = Player(*[int(self.level_manager.fileObjects[1][i]) for i in range(1,3)])

        setattr(self.level_manager,"player",self.player)
        setattr(self.player,"details",self.details)

    def run(self):
        inst = GameInstance(self.player,self.level_manager,self.details)
        inst.run()

class SpriteManager:
    def __init__(self,player):
        self.player = player
        self.init_sprites()
        
        self.direction = True # rightwards facing is default
        self.walk_state = 4
        self.sprint_state = 2
        self.old_velx = self.player.velx
        self.old_y = self.player.y

    def get_sprite(self):
        if self.player.velx * self.old_velx < 0: # if both multiply to make a negative number, there has been a sign change
            self.direction = not self.direction

        if self.player.crouching:
            return self.sprites[self.direction][6]

        if not self.player.velx * self.old_velx and self.player.velx < 0:
            self.direction = False

        vely = 0 if not self.player.y - self.old_y else self.player.vely

        if all(not i for i in [self.player.velx,vely]):
            return self.sprites[self.direction][0]

        if not vely and any(self.player.rect.colliderect(r) for r in self.player.rects):
            if -0.7 * self.player.velx_cap < self.player.velx < 0.7 * self.player.velx_cap:
                self.walk_state += 1

                if self.walk_state > 20:
                    self.walk_state = 0

                return self.sprites[self.direction][self.walk_state//10 + 1]

            else:
                self.sprint_state += 1

                if self.sprint_state > 10:
                    self.sprint_state = 0

                return self.sprites[self.direction][self.sprint_state//5 + 1]

        return self.sprites[self.direction][5]

    def update(self):
        if self.player.velx:
            self.old_velx = self.player.velx

        self.old_y = self.player.y

    def init_sprites(self):
        self._sprites = pygame.Surface([525,50], pygame.SRCALPHA, 32).convert_alpha()
        self._sprites.blit(pygame.image.load("sprites.png").convert_alpha(),(0,0))
        self.Rsprites = [self._sprites.subsurface(x*self.player.width,0,self.player.width,self.player.height) for x in range(21)]
        self.Lsprites = [pygame.transform.flip(s,1,0) for s in self.Rsprites]
        self.sprites = [self.Lsprites,self.Rsprites]
