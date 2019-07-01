import Colours
import pygame
import sys

#A1 = for debugging purposes
pygame.font.init()
f = pygame.font.SysFont("Garamond MS",20)

class Level:
    def __init__(self,init_level,details):
        self.current_level = init_level
        self.save_level = init_level
        self.details = details

    def load(self,from_save=None):
        with open(f"level_info/level{self.current_level if from_save is not None else self.save_level}.txt","r") as f:
            self.fileObjects = [i.split(" ") for i in f.read().split("\n")]

    def handle(self,keys):
        if keys[pygame.K_a]:
            self.player.movex(-5)

        if keys[pygame.K_d]:
            self.player.movex(5)

        if keys[pygame.K_SPACE] and self.player.can_jump:
            self.player.jump()
            self.player.can_jump = False

        if keys[pygame.K_LCTRL]:
            self.player.velx = 0

    def draw(self,surf):
        surf.fill(getattr(Colours,self.fileObjects[0][1],(255,255,255)))

        x_offset = self.details.size[0]/2 - self.player.rect.centerx
        y_offset = self.details.size[1]/2 - self.player.rect.centery

        for line in self.fileObjects[2:]:
            if line[1] == "Rect":
                pygame.draw.rect(surf,getattr(Colours,line[-1]),[float(line[2])+x_offset,float(line[3])+y_offset,float(line[4]),float(line[5])],0)

class GameInstance:
    def __init__(self,player,level,details):
        self.player = player
        self.level = level
        self.details = details
        self.player.update_level(self.level.fileObjects[2:])
        self.clock = pygame.time.Clock()

        #A1
        self._coords = True

    @property
    def lvl(self):
        return self.level

    @lvl.setter
    def lvl(self,new):
        self.level = new
        self.player.update_level(self.level.fileObjects[2:])

    def run(self):
        while True: 
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #A1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    self._coords = not self._coords

            self.level.handle(pygame.key.get_pressed())
            self.level.draw(self.details.surf)
            self.player.draw(self.details.surf)
            self.player.update()

            #A1
            if self._coords:
                self.details.surf.blit(f.render(f"x: {int(self.player.x)}",True,(0,0,0)),(10,10))
                self.details.surf.blit(f.render(f"y: {int(self.player.y)}",True,(0,0,0)),(10,25))
                self.details.surf.blit(f.render(f"vx: {int(self.player.velx)}",True,(0,0,0)),(10,40))
                self.details.surf.blit(f.render(f"vy: {int(self.player.vely)}",True,(0,0,0)),(10,55))

            pygame.display.flip()
