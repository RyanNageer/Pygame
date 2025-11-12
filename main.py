import pygame
import sys
from game import Game

g = Game()


while g.running: # while the game is running, we can run game_loop(self)
    g.curr_menu.display_menu()
    #g.intro_screen()
    # g.playing = True # set game to playing so our game loop runs
    #g.new() Already called in menu.py when the user selects start
    #g.main() already called in menu.py when the user selects start
    # g.game_over() 

pygame.quit() # When the game is no longer running we can safely exit
sys.exit()