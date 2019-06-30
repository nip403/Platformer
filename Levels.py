import Colours
import pygame
import sys

class Level:
    def __init__(self,player,init_level):
        self.player = player
        self.current_level = init_level
        self.save_level = init_level

    def load(self,from_save=None):
        with open(f"level{self.current_level if from_save is not None else self.save_level}.txt","r") as f:
            self.fileObjects = [i.split(" ") for i in f.read().split("\n")]

    def handle(self,keys):
        if keys[pygame.K_a]:
            self.player.velx -= 5

        if keys[pygame.K_d]:
            self.player.velx += 5

        if keys[pygame.K_SPACE] and not self.player.accy < 0 and self.player.can_jump:
            self.player.vely -= 40
            self.player.can_jump = False

    def draw(self,surf):
        surf.fill(getattr(Colours,self.fileObjects[0][1],(255,255,255)))

        for line in self.fileObjects[1:]:
            if line[1] == "Rect":
                pygame.draw.rect(surf,getattr(Colours,line[-1]),list(map(int,line[2:6])),0)

class GameInstance:
    def __init__(self,player,level,details):
        self.player = player
        self.level = level
        self.details = details

    def run(self):
        while True: 
            self.details.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.handle(pygame.key.get_pressed())
            self.level.draw(self.details.surf)
            self.player.draw(self.details.surf)
            self.player.update(self.level.fileObjects[1:])

            pygame.display.flip()
