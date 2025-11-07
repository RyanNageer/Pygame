import pygame
from config import *
from game import *
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert() # self.sheet is going to be the loaded image containing the sprite sheet, convert loads the image in faster so our game doesnt slow down

    def get_sprite(self, x, y, width, height): # cut out sprite from sprite sheet
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height)) # selects cutout from sprite sheet image and blits that particular sprite from the image to the screen
        sprite.set_colorkey(BLACK) # Set color key so we don't have a black background
        return sprite 
class Player(pygame.sprite.Sprite): # Layer 3
    def __init__(self, game, x, y): # game object, and coordinates to position the player at

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups) # calls init for inherited class, by passing in self.groups we add the player to the all sprites group

        self.x = x * TILESIZE # everything will be 32x32 pixels
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        # image_to_load = pygame.image.load("img/single2.png")
        # self.image = pygame.Surface([self.width, self.height]) # get an image that can later be drawn to the screen
        # self.image.set_colorkey(BLACK) # makes the specified color transparent
        # self.image.blit(image_to_load, (0,0)) # draw the image we've loaded in onto a surface
        
        # x position in the sprite sheet, y position in the spritesheet, x amount of pixels across, y amount of pixels down. width & height == 32
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) # calling get_sprite() from the Spritesheet class we made. referring to the Spritesheet object from the Spritesheet class we created above, we created the object in our __init__ function for the game class

        self.rect = self.image.get_rect() # set self.rect to be same size of the player
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change # once we see a change in position due to movement
        self.collide_blocks('x') # we can check for collision
        self.rect.y += self.y_change # change is a temporary variable of sorts and we use it to update the actual rectangle that refers to the player
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # if left arrow key pressed
            self.x_change -= PLAYER_SPEED # reduce the x axis to move the player left
            self.facing = 'left'
        if keys[pygame.K_RIGHT]: # if left arrow key pressed
            self.x_change += PLAYER_SPEED # reduce the x axis to move the player left
            self.facing = 'right'
        if keys[pygame.K_UP]: # if left arrow key pressed
            self.y_change -= PLAYER_SPEED # reduce the y axis to move the player up
            self.facing = 'up'
        if keys[pygame.K_DOWN]: # if left arrow key pressed
            self.y_change += PLAYER_SPEED # increase the y axis to move the player down
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill() # remove player from allsprites group
            self.game.playing = False # exits the game

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) # function from sprite library, checks if the rect of one sprite intersects with the rect of another sprite
            # Third parameter (one marked false) asks if you want to delete the sprite when it has a collision
            if hits:
                if self.x_change > 0: # hits[0] is the wall we're colliding with
                    self.rect.x = hits[0].rect.left - self.rect.width # because we takeaway the width of the rectangle, this creates the collision effect so the player cant walk on top the bock
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right


        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        # copied and pasted from pygame rpg tutorial #6 description
        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing == "down":
            if self.y_change == 0: # if we're standing still, set player to static image
                self.image = self.game.character_spritesheet.get_sprite(3,2, self.width, self.height)
            else: # if we are currently moving
                    self.image = down_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0: # if we're standing still, set player to static image
                self.image = self.game.character_spritesheet.get_sprite(3,34, self.width, self.height)
            else: # if we are currently moving
                    self.image = up_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0: # if we're standing still, set player to static image
                self.image = self.game.character_spritesheet.get_sprite(3,98, self.width, self.height)
            else: # if we are currently moving
                    self.image = left_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0: # if we're standing still, set player to static image
                self.image = self.game.character_spritesheet.get_sprite(3,66, self.width, self.height)
            else: # if we are currently moving
                    self.image = right_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE # x * TILESIZE converts from “tile index on the map” → “actual on-screen pixel position,”
        self.y = y * TILESIZE
        self.width = TILESIZE # makes an enemy exactly one tile big.
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30) # moving randomly between 7 and 30 pixels


        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK) # remove background of image

        self.rect = self.image.get_rect() # rectangle that holds the enemy's position. self.all_sprites.draw(self.screen) uses this to draw it to the screen at the right position.
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED # take away from x_change
            self.movement_loop -= 1 # subtract from movement loop
            if self.movement_loop <= -self.max_travel: #negative bc movement loop is being DECREASED # if enemy moves as far left as its set to go (only supposed to move between 7 and 30)
                self.facing = 'right' # then it faces right
        
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]
        # copied and pasted from pygame rpg tutorial #6 description
        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing == "down":
            if self.y_change == 0: # if we're standing still, set player to static image
                self.image = self.game.enemy_spritesheet.get_sprite(3,2, self.width, self.height)
            else: # if we are currently moving
                    self.image = down_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0: # if we're standing still, set player to static image
                self.image = self.game.enemy_spritesheet.get_sprite(3,34, self.width, self.height)
            else: # if we are currently moving
                    self.image = up_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0: # if we're standing still, set player to static image
                self.image = self.game.enemy_spritesheet.get_sprite(3,98, self.width, self.height)
            else: # if we are currently moving
                    self.image = left_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0: # if we're standing still, set player to static image
                self.image = self.game.enemy_spritesheet.get_sprite(3,66, self.width, self.height)
            else: # if we are currently moving
                    self.image = right_animations[math.floor(self.animation_loop)] # pull animation from down_animations list
                    self.animation_loop += 0.1 # every 10 frames the animation will change (0.1 * 10 = 1), animations are in indexes 0, 1 and 2
                    if self.animation_loop >= 3: # when its greater than or equal to 3 we reset the animation back to 1
                        self.animation_loop = 1


class Block(pygame.sprite.Sprite): # Layer 2
    def __init__(self, game, x, y): # game object and position on the tilemap

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE # Every sprite needs an image and rectangle
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        #self.image = pygame.Surface([self.width, self.height]) # image will always be 32 pixels long and wide 
        #self.image.fill(BLUE)

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite): # Layer 1
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups) # sets up all the sprite internals (so you get methods like .add(), .kill(), .groups()) and automatically adds the sprite to any Group objects you pass

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height) # get the image
        self.rect = self.image.get_rect() # create a rectangle and makes it the same size as self.image
        self.rect.x = self.x # assign the top left coorinates for the rectangle
        self.rect.y = self.y