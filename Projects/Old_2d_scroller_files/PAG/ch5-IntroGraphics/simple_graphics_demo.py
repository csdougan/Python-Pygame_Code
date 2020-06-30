#import required libraries
import pygame
#initialise pygame libraries
pygame.init()

#define some colours

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

#define value of PI for drawing circles etc
PI = 3.141592653

#define & create game window
size = (400,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Simple Graphics Demo")

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

	# draw 5 px wide line from 0,0 to 100,100
	pygame.draw.line(screen, GREEN, [0,0],[100,100],5)

	#draw several lines from 0,10 to 100,100
	for y_offset in range(0,100,10):
		pygame.draw.line(screen, RED, [0,10 + y_offset], [100,110 + y_offset], 5)

	# draw a rectangle
	pygame.draw.rect(screen, BLACK, [20,20,250,100], 2)

	# draw an ellipse using rectangle as outside boundaries
	pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)

	# draw an arc as part of an ellipse
	# use radians to determine what angle to draw
	pygame.draw.arc(screen, BLACK, [20,220,250,200], 0, PI/2,2)
	pygame.draw.arc(screen, GREEN, [20,220,250,200], PI/2,PI,2)
	pygame.draw.arc(screen, BLUE,  [20,220,250,200], PI,3*PI/2,2)
	pygame.draw.arc(screen, RED,   [20,220,250,200], 3*PI/2,2*PI,2)

	# this draws triangle using polygon command
	pygame.draw.polygon(screen, BLACK, [[100,100],[0,200],[200,200]],5)

	# select font to use 
	font = pygame.font.SysFont('Calibri',25,True,False)

	#Render text; True means use anti-aliasing
	text = font.render("My text", True, BLACK)

	#put image of text on screen
	screen.blit(text,[250,250])
	
	# update screen

	pygame.display.flip()

	# limit to 60FPS
	clock.tick(60)

	
pygame.quit()

