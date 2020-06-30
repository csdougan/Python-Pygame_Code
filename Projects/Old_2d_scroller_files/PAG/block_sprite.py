import pygame
import random

#Define some colours
BLACK = (000,000,000)
WHITE = (255,255,255)
RED   = (255,000,000)
GREEN = (000,255,000)
BLUE  = (000,000,255)


# Create a 'Block' sprite which inherits the
# properties of the default pygame Sprite class
class Block(pygame.sprite.Sprite):
	def __init__(self, colour, width, height):
		#call the constructor of the parent Sprite class
		pygame.sprite.Sprite.__init__(self)
		#define the image for the Sprite - in this case
		#an image isn't being loaded so we use a blank
		#surface and fill with the colour specified
		self.width = width
		self.height = height
		self.image = pygame.Surface([width,height])
		self.image.fill(colour)
		#get a rectangle containing the dimensions of sprite image
		self.rect = self.image.get_rect()

############ Main Program section ############

#set up initial environment
pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# create a sprite list to contain all block sprites
block_list = pygame.sprite.Group()
# create a sprite list to contain all sprites in game
all_sprites_list = pygame.sprite.Group()
		
# create block sprites
for i in range(50):
	#this represents a block
	block = Block(BLACK, 20, 15)
	
	#set a random location for the blocks
	block.rect.x = random.randrange(screen_width-block.width)
	block.rect.y = random.randrange(screen_height-block.height)

	#add the block to the list of block sprites
	block_list.add(block)
	all_sprites_list.add(block)
	
# Create a RED player block
player = Block(RED, 20, 15)
all_sprites_list.add(player)

# Set up Game Loop
done = False
clock = pygame.time.Clock()
score = 0

### MAIN GAME LOOP #####

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	# Clear the screen
	screen.fill(WHITE)
	
	# get current mouse position
	pos = pygame.mouse.get_pos()
	# set players rectangle to be at current mouse position
	player.rect.x = pos[0]
	player.rect.y = pos[1]
	
	all_sprites_list.draw(screen)
	clock.tick(60)
	pygame.display.flip()
pygame.quit()
	
	
	
