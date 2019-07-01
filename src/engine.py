from Levels import *
import pygame

#add skins
class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.velx = 0
        self.vely = 0

        self.velx_cap = 10
        self.vely_cap = 25

        self.gravity = 0.2
        self.friction = 0.05
        self.mass = 1

        self.width = 25
        self.height = 50

        self._update_rect()
        self.can_jump = True
        self.init_sprites()
        self.direction = True # rightwards facing is default

        self.allow_wall_jump = False

        self.walk_state = 4
        self.sprint_state = 2
        self.old_velx = self.velx
        self.old_y = y

    def init_sprites(self):
        self._sprites = pygame.Surface([525,50], pygame.SRCALPHA, 32).convert_alpha()
        self._sprites.blit(pygame.image.load("sprites.png").convert_alpha(),(0,0))
        self.Rsprites = [self._sprites.subsurface(x*self.width,0,self.width,self.height) for x in range(21)]
        self.Lsprites = [pygame.transform.flip(s,1,0) for s in self.Rsprites]
        self.sprites = [self.Lsprites,self.Rsprites]

    def _set_details(self,details):
        self.details = details

    def jump(self):
        self.vely = -15

    def movex(self,dx):
        self.velx += dx

    def draw(self,surf):
        surf.blit(self.get_sprite(),(self.details.size[0]/2 - self.width/2,self.details.size[1]/2 - self.height/2))

    def get_sprite(self):
        if self.velx * self.old_velx < 0: # if both multiply to make a negative number, there has been a sign change
            self.direction = not self.direction

        vely = 0 if not self.y - self.old_y else self.vely

        if all(not i for i in [self.velx,vely]):
            return self.sprites[self.direction][0]

        if not vely and any(self.rect.colliderect(r) for r in self.rects):
            if -0.5 * self.velx_cap < self.velx < 0.5 * self.velx_cap:
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

    def _update_rect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def update_level(self,objects):
        self.rects = [pygame.Rect(*list(map(int,o[2:6]))) if o[1] == "Rect" else pygame.Rect(int(o[2])-int(o[4]),int(o[3])-int(o[4]),int(o[4])*2,int(o[4])*2) for o in objects]

    def update(self):
        if self.velx:
            self.old_velx = self.velx

        self.old_y = self.y

        if abs(self.velx) < self.friction:
            self.velx = 0
        else:
            self.velx -= self.friction if self.velx > 0 else -self.friction

        if abs(self.vely) < self.friction:
            self.vely = 0
        else:
            self.vely -= self.friction if self.vely > 0 else -self.friction

        if not any(self.rect.colliderect(r) and (set(range(self.x,self.x+self.width)) & set(range(r.left,r.right))) for r in self.rects):
            self.vely += self.gravity

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
            self._update_rect()

            if any(self.rect.colliderect(r) for r in self.rects):
                self.x -= 1 if self.velx > 0 else -1

                if self.allow_wall_jump:
                    self.can_jump = True

                break

        for y in range(self.y+1,int(self.y+self.vely+1)) if self.vely > 0 else reversed(range(int(self.y+self.vely),self.y)):
            self.y = y
            self._update_rect()

            if any(self.rect.colliderect(r) for r in self.rects):
                self.y -= 1 if self.vely > 0 else -1

                if self.vely < 0:
                    self.vely = 0

                if any(self.rect.colliderect(r) and self.rect.top - r.bottom < -1 for r in self.rects):
                    self.can_jump = True

                break

class Game:
    def __init__(self,player,details):
        self.player = player
        self.surf = details.surf
        self.clock = details.clock
        self.size = details.size
        self.details = details

        # load level 0 (tutorial)
        self.level_manager = Level(self.player,0,self.details)
        self.player._set_details(self.details)

    def run(self):
        self.level_manager.load()
        inst = GameInstance(self.player,self.level_manager,self.details)
        inst.run()
