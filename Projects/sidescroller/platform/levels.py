import pygame
import random
import constants
import platforms
import collectcoin
from Actor import Actor

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None
    collect_list = None

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
	self.collect_list = pygame.sprite.Group()
        self.player = player

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
	self.collect_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        # Draw all the sprite lists that we have
	self.collect_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
	
	self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

	for collect in self.collect_list:
		collect.rect.x += shift_x
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_01.jpg").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -4500

        # Array with type of platform, and x, y location of the platform.
        level = [ ["ac_fan", 500, 500],
                  ["ac_fan", 570, 500],
                  ["ac_fan", 640, 500],
                  ["ac_fan", 800, 400],
                  ["ac_fan", 870, 400],
                  ["ac_fan", 940, 400],
                  ["ac_fan", 1000, 500],
                  ["ac_fan", 1070, 500],
                  ["ac_fan", 1140, 500],
                  ["ac_fan", 1120, 280],
                  ["ac_fan", 1190, 280],
                  ["ac_fan", 1260, 280],
                  ]

	collect = [ ["disk_02", 500, 400],
			["disk_02", 600, 400],
			["disk_02", 700, 400],
			["disk_02", 800, 300],
			["disk_02", 900, 300],
			["disk_02", 1000, 200],
			["disk_02", 1100, 200],]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            #block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform("ac_fan")
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

	x=random.randrange(0,constants.SCREEN_WIDTH)
	tmp_npc=Actor("droid_walk.png",x)
	tmp_npc.level = self
	self.enemy_list.add(tmp_npc)
	
	for disktoken in collect:
		collectCoin = collectcoin.CollectCoin(disktoken[0])
		collectCoin.rect.x = disktoken[1]
		collectCoin.rect.y = disktoken[2]
		self.collect_list.add(collectCoin)


# Create platforms for the level

