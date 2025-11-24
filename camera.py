import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod # Inheriting from ABC tells Python: this class may contain abstract methods and can be treated as an abstract base class

#Camera needs to be able to switch between 3 modes: Auto movement, follow the player, and static border mode where it doesnt move
class Camera: 
    def __init__(self, player):
        self.player = player
        self.offset = vec(0,0) # What we use to frame our camera in the right position
        self.offset_float = vec(0,0) # stores precise position of our offset
        self.DISPLAY_W, self.DISPLAY_H = 1920, 1080
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.ground_y + 20)

    def setmethod(self, method): # Picks the method we're using, whether it be auto, follow, or border
        self.method = method

    def scroll(self): # Abstract Class, strategy pattern
        self.method.scroll()

class CamScroll(ABC): # Inheriting from ABC tells Python: this class may contain abstract methods and can be treated as an abstract base class
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player
 
    @abstractmethod # @abstractmethod – marks methods that must be overridden, if the line under it isn't filled then python will report something has gone wrong.
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

                      # we subtract the position of the player by the position of the camera in order to put the camera in the correct spot at the position of the player
    def scroll(self): # if we subtract the position of the camera by an offset the player will always be in the middle of the screen
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.x += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
        
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.x += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x) # handles the left border # to stop the camera from scrolling in the left when we hit the border of the play area
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)
        
class Auto(CamScroll): # Screen moving independently of the player
    def _init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
        
    def scroll(self):
        self.camera.offset.x += 1 # move the camera by one pixel every frame, positive moves it right, negative moves it left