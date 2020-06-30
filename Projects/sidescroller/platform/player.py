"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0
    playerFPS = 60 # by dividing the gameFPS by this we get the value of when to increment the player sprite
    gameFPS = 60 # this will be passed in later, for now I'm hardcoding it

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    stand_frames_l = []
    stand_frames_r = []
    current_frame = 0
    timeLastUpdate = 0
    walking = False
    jumping = False




    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
     #   pygame.sprite.Sprite.__init__(self)



	pygame.sprite.Sprite.__init__(self)
	#load the sprite sheet
	#sprite_sheet = SpriteSheet(filename)
        sprite_sheet = SpriteSheet("p1_walk.png")
	#specify how many frames are contained in the sprite sheet
	frames_in_walk_cycle=8
	#work out the width of each individual frame
	sprite_width=sprite_sheet.rect.width / frames_in_walk_cycle
	#as all sprites are on one line the height of each frame is the same as the sprite sheet
	sprite_height=sprite_sheet.rect.height
		
	#cycle through each frame in sprite sheet
	for i in range(frames_in_walk_cycle):
		#assign current frame to a temporary frame image
		temp_frame = sprite_sheet.get_image(i * sprite_width, 0, sprite_width, sprite_height)
		#add current frame to array of right-facing walking frame images
		self.walking_frames_r.append(temp_frame)
		#flip frame over on x-axis to get left facing image
		temp_frame = pygame.transform.flip(temp_frame, True, False)
		#add current frame to array of left-facing wlaking frame images
		self.walking_frames_l.append(temp_frame)
        

	sprite_sheet = SpriteSheet("p1_stand2.png")
	frames_in_stand_cycle = 8

	#work out the width of each individual frame
	sprite_width=sprite_sheet.rect.width / frames_in_stand_cycle
	#as all sprites are on one line the height of each frame is the same as the sprite sheet
	sprite_height=sprite_sheet.rect.height
	#cycle through each frame in sprite sheet
	for i in range(frames_in_stand_cycle):
		#assign current frame to a temporary frame image
		temp_frame = sprite_sheet.get_image(i * sprite_width, 0, sprite_width, sprite_height)
		#add current frame to array of right-facing walking frame images
		self.stand_frames_r.append(temp_frame)
		#flip frame over on x-axis to get left facing image
		temp_frame = pygame.transform.flip(temp_frame, True, False)
		#add current frame to array of left-facing wlaking frame images
		self.stand_frames_l.append(temp_frame)


	# Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

	gameTime=pygame.time.get_ticks()
	timeElapsed=0
	if self.timeLastUpdate == 0:
		self.timeLastUpdate = gameTime

	timeElapsed = gameTime - self.timeLastUpdate	

        pos = self.rect.x + self.level.world_shift


        if self.direction == "R" and self.walking == False:
            if (timeElapsed > self.playerFPS):
		self.current_frame += 1
		self.current_frame %= (len(self.stand_frames_l))
		self.timeLastUpdate = gameTime
            self.image = self.stand_frames_r[self.current_frame]
        elif self.direction == "L" and self.walking == False:
            if (timeElapsed > self.playerFPS):
		self.current_frame += 1
		self.current_frame %= (len(self.stand_frames_l))
		self.timeLastUpdate = gameTime
            self.image = self.stand_frames_l[self.current_frame]
        elif self.direction == "R" and self.walking == True:
            if (timeElapsed > self.playerFPS):
		self.current_frame += 1
		self.current_frame %= (len(self.walking_frames_l))
		self.timeLastUpdate = gameTime
            self.image = self.walking_frames_r[self.current_frame]
        elif self.direction == "L" and self.walking == True:
            if (timeElapsed > self.playerFPS):
		self.current_frame += 1
		self.current_frame %= (len(self.walking_frames_l))
		self.timeLastUpdate = gameTime
            self.image = self.walking_frames_l[self.current_frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

	# Check if we hit a token
	collect_hit_list = pygame.sprite.spritecollide(self, self.level.collect_list, True)

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"
	self.walking = True

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"
	self.walking = True

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
	self.walking = False
