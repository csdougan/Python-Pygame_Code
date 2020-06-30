import pygame
import random

global BLACK, WHITE, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_FLOOR

#set up constants for screen dimensions and colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_FLOOR = SCREEN_HEIGHT-100

#create an object to act as a reference for our spritesheet
class SpriteSheet(object):
	def __init__(self, filename):
		#load the spritesheet specified by filename 
		self.sprite_sheet = pygame.image.load(filename).convert()
		#get dimension information for the sprite sheet
		self.rect = self.sprite_sheet.get_rect()

	#this function returns a section of the spritesheet as an image
	def get_image(self,x,y,width,height):
		#create a blank surface to contain the sprite we're going to pull from the spritesheet
		image = pygame.Surface([width,height]).convert()
		#copy the specified section of spritesheet to the "image" surface
		image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
		#set the colour key of the sprite that's going to be returned
		image.set_colorkey(WHITE)
		#return back the section of the sprite sheet we've specified
		return image

class Player(pygame.sprite.Sprite):
	#set up two values to use to move the sprite along x and y axis
	#0 means the sprite isnt moving along that axis.
	change_x = 0
	change_y = 0

	#these arrays are to be used to contain the frames for the walk cycle
	walking_frames_left = []
	walking_frames_right = []
	direction = "R"

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#load the sprite sheet
		sprite_sheet = SpriteSheet("bret_run_sprite_sheet.png")
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
			self.walking_frames_right.append(temp_frame)
			#flip frame over on x-axis to get left facing image
			temp_frame = pygame.transform.flip(temp_frame, True, False)
			#add current frame to array of left-facing wlaking frame images
			self.walking_frames_left.append(temp_frame)

		#set initial frame image	
		self.image = self.walking_frames_right[0]

		#create rectangle object to hold frame info
		self.rect = self.image.get_rect()

	def update(self):
		
		#move left/right
		self.fall_from_jump()
		self.rect.x += self.change_x
		pos = self.rect.x
		
		#set how many pixels we need to move by before walk cycle frame changes
		pixels_per_frame=30

		# This determines what the current walk cycle frame is.   This is a bit of a fudge -
		# basically every position in the 'game world' has a walk cycle frame assigned to it
		# - this is worked out by dividing the current position (pos) by the number of pixels we
		# need to move by before the frame changes (pixels_per_frame) - to ensure that this always
		# gives a value within the range of walk cycle frames available, we divide that number by
		# the number of frames available and set the current frame to the remainder (done using 'modulus')
		
		if self.direction == "R": # if heading right, use the right-facing frames
			frame = (pos // pixels_per_frame) % len(self.walking_frames_right)
			self.image = self.walking_frames_right[frame]
		else: # otherwise use the left-facing frames
			frame = (pos // pixels_per_frame) % len(self.walking_frames_left)
			self.image = self.walking_frames_left[frame]

		# Move up/down
		self.rect.y += self.change_y
			
	# if player directs character to go left, then change x position by -6
	def go_left(self):
		self.change_x = -6
		self.direction = "L"
	
	# if player directs character to go right, then change x position by +6
	def go_right(self):
		self.change_x = 6
		self.direction = "R"
	
	def fall_from_jump(self):
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += .5
		
		if self.rect.y >= GAME_FLOOR - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = GAME_FLOOR - self.rect.height
			
	def jump(self):
			# check player is standing on the floor
			if self.rect.bottom >= GAME_FLOOR:
				self.change_y = -10
			
	# if player stops directing character, then set the amount to change x by to 0
	def stop(self):
		self.change_x = 0


def main():
	# set up initial game environment
	global SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, BLUE
	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
	pygame.display.set_caption("Walk Cycle Test")

	# create player
	player = Player()

	# set players initial x-axis position
	player.rect.x = 340
	# set players initial y-axis position to be at bottom of screen
	player.rect.y = GAME_FLOOR - player.rect.height
	
	# create a group to hold our sprites
	active_sprite_list = pygame.sprite.Group()
	# add player sprite to the sprite group
	active_sprite_list.add(player)

	# set up initial game loop 
	done = False
	clock = pygame.time.Clock()

	### - MAIN GAME LOOP - ###
	while not done:
		# look for user input
		for event in pygame.event.get():
			# exit if user closes window
			if event.type == pygame.QUIT:
				done = True
			
			# check to see if a key is pressed down
			if event.type == pygame.KEYDOWN:
				# if left arrow is pressed, then go left
				if event.key == pygame.K_LEFT:
					player.go_left()
				# if right arrow is pressed, go right
				if event.key == pygame.K_RIGHT:
					player.go_right()
				# if up arrow is pressed, then jump
				if event.key == pygame.K_UP:
					player.jump()
				
			# check for when user releases key
			if event.type == pygame.KEYUP:
				# if the depressed key was the left arrow and the amount to move the
				# player character by is still set to a non zero amount, then stop the player
				# - this is to prevent the player character from continuing to move after the key is
				#   released.
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.stop()
				# same as above but for right arrow
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		### Draw current level in buffer ####
		screen.fill(BLACK)
		### Update Sprite Positions in buffer ###
		active_sprite_list.update()
		### Draw Sprites ###
		active_sprite_list.draw(screen)

		### Set game FPS ###
		clock.tick(60)

		### Draw buffer to screen ###
		pygame.display.flip()
	
	# Main game loop has exited here so we can tidy up and exit.
	pygame.quit()

main()
		
		
