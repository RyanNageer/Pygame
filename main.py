from game import Game

g = Game()


while g.running: # while the game is running, we can run game_loop(self)
    g.curr_menu.display_menu()
    # g.playing = True # set game to playing so our game loop runs
    g.game_loop()