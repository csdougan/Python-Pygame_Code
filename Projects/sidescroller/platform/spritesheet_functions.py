"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame

import constants

#class SpriteSheet(object):
#    """ Class used to grab images out of a sprite sheet. """
#    # This points to our sprite sheet image
#    sprite_sheet = None#
#
 #   def __init__(self, file_name):
 #       """ Constructor. Pass in the file name of the sprite sheet. """
#
 #       # Load the sprite sheet.
  #      self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
#
#
#    def get_image(self, x, y, width, height):
#        """ Grab a single image out of a larger spritesheet
#            Pass in the x, y location of the sprite
#            and the width and height of the sprite. """#

#        # Create a new blank image
 #       image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
  #      image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
   #     image.set_colorkey(constants.BLACK)

        # Return the image
    #    return image

class SpriteSheet(object):
	def __init__(self, filename):
		#load the spritesheet specified by filename 
		self.sprite_sheet = pygame.image.load(filename).convert_alpha()
		#get dimension information for the sprite sheet
		self.rect = self.sprite_sheet.get_rect()

	#this function returns a section of the spritesheet as an image
	def get_image(self,x,y,width,height):
		#create a blank surface to contain the sprite we're going to pull from the spritesheet
		image = pygame.Surface([width,height]).convert()
		#copy the specified section of spritesheet to the "image" surface
		image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
		image.set_colorkey(constants.BLACK)
		
		#set the colour key of the sprite that's going to be returned
		#image.set_colorkey(WHITE)
		#return back the section of the sprite sheet we've specified
		return image

