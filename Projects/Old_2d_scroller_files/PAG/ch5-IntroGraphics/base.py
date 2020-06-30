#import required libraries
import pygame
#initialise pygame libraries
pygame.init()

#define some colours

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

#define value of PI for drawing circles etc
PI = 3.141592653

#define & create game window
size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game title goes here")

#set a variable to use for creating game loop
done = False

#used to manage screen refresh rate
clock = pygame.time.Clock()

#### - Main Game Loop Starts Here - ####

while not done:
	#check for some kind of user input
	for event in pygame.event.get():
		# handle if user selects close window 
		if event.type == pygame.QUIT:
			done = True
	
	#### - Game Logic Section - ####


	#### - Drawing Code Section - ####

	# fill screen with white initially
	screen.fill(WHITE)

	# update screen

	pygame.display.flip()

	# limit to 60FPS
	clock.tick(60)

	
pygame.quit()

