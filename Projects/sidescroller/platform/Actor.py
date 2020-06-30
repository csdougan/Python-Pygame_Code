import pygame
import constants
import random
from spritesheet_functions import SpriteSheet

class Actor(pygame.sprite.Sprite):
	#set up two values to use to move the sprite along x and y axis
	#0 means the sprite isnt moving along that axis.
	change_x = 0
	change_y = 0
	left_boundary = 200
	right_boundary = 800
	level = None

	playerFPS = 60 


	#these arrays are to be used to contain the frames for the walk cycle
	walking_frames_left = []
	walking_frames_right = []
	stand_frames_l = []
	stand_frames_r = []
	current_frame = 0
	timeLastUpdate = 0
	direction = "R"
	walking = True
	jumping = False


	def __init__(self,filename,start_x=0):
		pygame.sprite.Sprite.__init__(self)
		#load the sprite sheet
		sprite_sheet = SpriteSheet(filename)
		#specify how many frames are contained in the sprite sheet
		frames_in_walk_cycle=8
		#work out the width of each individual frame
		sprite_width=sprite_sheet.rect.width / frames_in_walk_cycle
		#as all sprites are on one line the height of each frame is the same as the sprite sheet
		sprite_height=sprite_sheet.rect.height
		
		#cycle through each frame in sprite sheet
		for i in reversed(range(frames_in_walk_cycle)):
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
		self.rect.y = constants.GAME_FLOOR - self.rect.height
		self.rect.x = start_x
		
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
		
		#if self.direction == "R": # if heading right, use the right-facing frames
		#	frame = (pos // pixels_per_frame) % len(self.walking_frames_right)
		#	self.image = self.walking_frames_right[frame]
		#else: # otherwise use the left-facing frames
		#	frame = (pos // pixels_per_frame) % len(self.walking_frames_left)
		#	self.image = self.walking_frames_left[frame]

		gameTime=pygame.time.get_ticks()
		timeElapsed=0
		if self.timeLastUpdate == 0:
			self.timeLastUpdate = gameTime

		timeElapsed = gameTime - self.timeLastUpdate	

		pos = self.rect.x + self.level.world_shift
        	if self.direction == "R" and self.walking == True:
            		if (timeElapsed > self.playerFPS):
				self.current_frame += 1
				self.current_frame %= (len(self.walking_frames_left))
				self.timeLastUpdate = gameTime
            		self.image = self.walking_frames_right[self.current_frame]
        	elif self.direction == "L" and self.walking == True:
            		if (timeElapsed > self.playerFPS):
				self.current_frame += 1
				self.current_frame %= (len(self.walking_frames_left))
				self.timeLastUpdate = gameTime
            		self.image = self.walking_frames_left[self.current_frame]


		# Move up/down
		self.rect.y += self.change_y
		self.auto_move()
		
	def auto_move(self):
		cur_pos = self.rect.x - self.level.world_shift	
		if self.direction == "R":
			self.go_right()
			if cur_pos >= self.right_boundary:
				self.direction = "L"
		else:
			self.go_left()
			if cur_pos <= self.left_boundary:
				self.direction = "R"


        # Check the boundaries and see if we need to reverse
        # direction.
		
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
		
		if self.rect.y >= constants.GAME_FLOOR - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = constants.GAME_FLOOR - self.rect.height
			
	def jump(self):
			# check player is standing on the floor
			if self.rect.bottom >= constants.GAME_FLOOR:
				self.change_y = -10
			
	# if player stops directing character, then set the amount to change x by to 0
	def stop(self):
		self.change_x = 0

