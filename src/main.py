#objective:
#get to the end whilst not dying
#time limit  
#avoid enemies and collect powerups
#prison theme? - rename

import pygame 
from engine import Player,Game

s = [1000,800]

pygame.init()
screen = pygame.display.set_mode(s,0,32,0)
clock = pygame.time.Clock()
pygame.display.set_caption("Adventurer Beta")

_details = type("Details",(),{"surf":screen,"clock":clock,"size":s})

def main(): 
    player = Player(250,250) 
    game = Game(player,_details)
    game.run()
    
if __name__ == "__main__":
    main()
