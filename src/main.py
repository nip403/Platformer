import pygame
from MainClasses import Player,Game

s = [1000,800]
pygame.init()
screen = pygame.display.set_mode(s,0,32,0)
clock = pygame.time.Clock()
pygame.display.set_caption("Platformer Alpha 0.0")

_details = type("Details",(),{"surf":screen,"clock":clock,"size":s})

def main():
    player = Player(250,250) 
    game = Game(player,_details)
    game.run()
    
if __name__ == "__main__":
    main()
