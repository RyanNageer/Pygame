import pygame # package

class Game(): 
    def __init__(self):
        pygame.init()
        self.running, self.player = True, False # game is running but player is not currently playing
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False # Controls for our menu initialized to false. Upon keystroke (ex. UP arrow) they will be set to true
        self.DISPLAY_W, self.DISPLAY_H = 480, 270 # width and height of our canvas
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H)) # Canvas(dimensions)
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H))) # we want player to see what we're drawing. so this line displays the canvas
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)

    def game_loop(self):
        while self.playing: # while player is playing
            self.check_events() # check for inputs
            if self.START_KEY: # if start key is pressed
                self.playing = False # breaks the while self.playing loop on line 15
            self.display.fill(self.BLACK) # reset our Canvas before drawing the next image. without this line it's like drawing on the same page in a flip book instead of turning to the next page
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2) # calling the draw_text function we made. we use font size 20 and 480/2 and 270/2 for our coordinates which should put the text in the center of the screen.
            self.window.blit(self.display, (0,0)) # "BLock Image Transfer" aka copy our canvas onto the visible window that our player sees (0,0) are our top-left XY coordinates
            pygame.display.update() # physically puts this on the monitor/computer screen
            self.reset_keys() # sets our flags back to false so we can accept new inputs
    
    
    def check_events(self):
        for event in pygame.event.get(): # checks what the player can do on the computer
            if event.type == pygame.QUIT: # checks if player quits game (for example, hits the X button)
                self.running, self.playing = False, False
            # check for keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # player has pressed the Enter key
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE: # player has pressed the Enter key
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN: # player has pressed the Enter key
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP: # player has pressed the Enter key
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.font_name, size) # Font(file_path=None, size=12)
        text_surface = font.render(text, True, self.WHITE) # render(text, antialias, color, background=None): creates a new Surface with the specified text rendered on it. draw text on a new Surface
        text_rect = text_surface.get_rect() # text_rect is a rectangle. within it lies our text. rectangle class has 4 main components, x, y, width, and height. this rectangle has the same width & height as our text surface
        text_rect.center = (x,y) # moves the text’s center point to (x, y) coordinates on the canvas (self.display). assigns a x and y position to the center of the rectangle. so it will center the text wherever we want it to be.
        self.display.blit(text_surface, text_rect) # blit(source, dest, area=None, special_flags=0) -> Rect # copy the pixels from text_surface onto our canvas self.display, at the position text_rect
