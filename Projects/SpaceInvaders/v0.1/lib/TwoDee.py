from pygame import *
import random, math


class Sprite:
	def __init__(self, gameEnv, *filename):
		#global last_sprite_created
		#last_sprite_created = self
		self.gameEnv = gameEnv
		gameEnv.last_sprite_created = self
		#self.screen = screenObject
		if len(filename) > 1 :
			self.is_sprite_animated = True
		else:
			self.is_sprite_animated = False
		self.sprite_frame=[]
		self.x = gameEnv.sprite_buffer_xpos
		self.y = gameEnv.sprite_buffer_ypos
		self.firstfile = filename[0]
		self.currentSpriteFrame = -1
		for sprite_file in filename:
			self.currentSpriteFrame += 1
			self.sprite_bitmap = image.load(sprite_file)
			self.sprite_bitmap = self.sprite_bitmap.convert_alpha()
			self.sprite_width = self.sprite_bitmap.get_width()
			self.sprite_height = self.sprite_bitmap.get_height()
			#self.sprite_bitmap.set_colorkey((0,0,0))
			self.buffer_x = gameEnv.sprite_buffer_xpos
			self.buffer_y = gameEnv.sprite_buffer_ypos
			# sprite_frame[x,0] = bitmap_object for that frame
			# sprite_frame[x,1] = width of current frame
			# sprite_frame[x,2] = height of current frame
			# sprite_frame[x,3] = x position in buffer allocated to current frame
			# sprite_frame[x,4] = y position in buffer allocated to current frame
			self.sprite_frame.append([self.sprite_bitmap,self.sprite_width,self.sprite_height,self.buffer_x,self.buffer_y])
			gameEnv.next_sprite_buffer_slot()
		 
		self.totalSpriteFrames = len(self.sprite_frame) # how many sprite frames are in the sequence
		self.lastSpriteFrame =  ( len(self.sprite_frame) - 1) # what is the reference number of the last sprite in the sequence
		self.totalSpritestoUse = len(self.sprite_frame)
		self.lastSpritetoUse = (len(self.sprite_frame) - 1)
		self.firstSpritetoUse = 0
					
		self.currentSpriteFrame = 0
		self.spriteOffset = 0
	
	def randomCurrentFrame(self,enable=False):
		if enable:
			self.spriteOffset = random.randrange(self.totalSpriteFrames)
		else:
			self.spriteOffset = 0
	
	def rotate(self,angle,frame_to_flip=-1):
		if frame_to_flip >= 0:
			if frame_to_flip > self.lastSpriteFrame:
				frame_to_flip = self.lastSpriteFrame
			self.sprite_frame[frame_to_flip][0] = transform.rotate(self.sprite_frame[frame_to_flip][0],angle)
		else:
			for i in range(self.totalSpriteFrames):
				self.sprite_frame[i][0] = transform.rotate(self.sprite_frame[i][0],angle)
	
	def set_sprite_frame_range(self,start_range=0,end_range=-1):
		if end_range == -1:
			self.lastSpritetoUse = self.lastSpriteFrame
		elif end_range > self.totalSpriteFrames:
			self.lastSpritetoUse = self.lastSpriteFrame
		else:
			self.lastSpritetoUse = end_range
		if (start_range < 0) or (start_range > self.lastSpriteFrame):
			self.firstSpritetoUse = 0
		else:
			self.firstSpritetoUse = start_range
		
	
	def flip_horizontal(self,frame_to_flip="-1"):
		if frame_to_flip >= 0:
			if frame_to_flip > self.lastSpriteFrame:
				frame_to_flip = self.lastSpriteFrame
			sprite_frame[frame_to_flip,0] = transform.flip(sprite_frame[frame_to_flip,0],True,False)
		else:
			for i in range(self.totalSpriteFrames):
				sprite_frame[i,0] = transform.flip(sprite_frame[i,0],True,False)
			
	def flip_vertical(self,frame_to_flip="-1"):
		if frame_to_flip >= 0:
			if frame_to_flip > self.lastSpriteFrame:
				frame_to_flip = self.lastSpriteFrame
			sprite_frame[frame_to_flip,0] = transform.flip(sprite_frame[frame_to_flip,0],False,True)
		else:
			for i in range(self.totalSpriteFrames):
				sprite_frame[i,0] = transform.flip(sprite_frame[i,0],False,True)
				
		
	def next_sprite_frame(self):
		# decrease the current sprite number by 1
		self.currentSpriteFrame += 1
		# use modulus to ensure that if a number greater than the total is given it will 'wrap around' to the beginning
		# i.e if the total number of sprites is 8 and a frame number 9 is used, this will be 'wrapped around' by the 
		# modulus ('%') function to become 1.
		self.currentSpriteFrame = int(float(self.currentSpriteFrame + self.spriteOffset) % (self.totalSpritestoUse))
	
	def previous_sprite_frame(self):
		# decrease the current sprite number by 1.
		self.currentSpriteFrame -= 1
		# use modulus to ensure that if a number less than 0 is given it will 'wrap around' to the end
		# i.e if the total number of sprites is 8 and a frame number -1 is used, this will be 'wrapped around' by the 
		# modulus ('%') function to become 7 (the sprite range here is 0-7)
		self.currentSpriteFrame = int(float(self.currentSpriteFrame + self.spriteOffset) % (self.totalSpritestoUse))
	
	def select_sprite_frame(self,selected_frame):
		# set the current sprite to the number specified
		self.currentSpriteFrame = selected_frame
		# use modulus to ensure that if a number greater than the total is given it will 'wrap around' to the beginning
		# i.e if the total number of sprites is 8 and a frame number 9 is used, this will be 'wrapped around' by the 
		# modulus ('%') function to become 1.
		self.currentSpriteFrame = int(float(self.currentSpriteFrame + self.spriteOffset) % (self.totalSpritestoUse))
	
	
	
	def set_position(self, xpos, ypos):
		self.x = xpos
		self.y = ypos

	
	def render(self):
			
			#check if a range has been set
			if (self.lastSpritetoUse != self.lastSpriteFrame) and (self.firstSpritetoUse != 0):		
				# work out how many sprites are in the range
				self.spritesInRange = (self.lastSpritetoUse - self.firstSpritetoUse)
				# work out what the current frame would be if the total range had been applied (i.e no custom range set)
				self.currentSpriteFrame = int(float(self.currentSpriteFrame + self.spriteOffset) % (self.totalSpriteFrames))
				# now use modulus to work out what the current frame would be if the range set was '1st sprite' to 'total frames in range'
				self.currentSpriteFrame = int(float(self.currentSpriteFrame) % (self.totalSpritestoUse))
				# add the number of the first sprite in the range to the current frame to shift it into the specified range
				self.currentSpriteFrame += self.firstSpritetoUse
			else:
				# this line below is to auto move the sprite into the next frame - hashed out as not required here
				#self.currentSpriteFrame = (int(math.ceil(  currentGameFrame.current_frame /  float(MAX_FRAME / self.totalSpriteFrames)  )) -1)
				self.currentSpriteFrame = (int(math.ceil(  self.gameEnv.currentGameTimer.current_frame /  float(self.gameEnv.max_frame / self.totalSpriteFrames)  )) -1)
				# set the current frame by using adding the current sprite to any 'random' offset used.  modulus is applied to 'wrap around'
				# the number if it exceeds the total number of sprites.
				
				self.displaySpriteFrame = int(float(self.currentSpriteFrame + self.spriteOffset) % (self.totalSpriteFrames))
				
			# display the sprite		
			self.gameEnv.gameScreen.screen.blit(self.sprite_frame[self.displaySpriteFrame][0], (self.x, self.y))

					
class GameTimer:
	def __init__(self,gameEnv):
		self.frameFont = font.SysFont("monospace", 24)
		self.frame_x = 100
		self.frame_y = 20
		self.current_frame = 0
		self.gameEnv = gameEnv
	def render(self):
		self.frameText = ("GF : %d" % self.current_frame)
		self.frameTextObj = self.frameFont.render(self.frameText, 1 ,(255,255,0))
		self.gameEnv.gameScreen.screen.blit(self.frameTextObj,(self.frame_x,self.frame_y))

class GameScore:
	def __init__(self, gameEnv):
		self.scoreFont = font.SysFont("monospace", 24)
		self.score = 0
		self.score_x = 450
		self.score_y = 20
		self.gameEnv = gameEnv
	def increase_score(self, points):
		self.score += points
	def render(self):
		self.scoreText = ("Score : %d" % self.score)
		self.scoreTextObj = self.scoreFont.render(self.scoreText, 1 ,(255,255,0))
		self.gameEnv.gameScreen.screen.blit(self.scoreTextObj,(self.score_x,self.score_y))

		
def move_sprite(sprite_to_move,move_x=0,move_y=0):
	sprite_to_move.set_position(sprite_to_move.x + move_x, sprite_to_move.y + move_y)
		
def relocate_sprite(sprite_to_relocate,new_x,new_y):
	sprite_to_relocate.x = new_x
	sprite_to_relocate.y = new_y
	

class Game_Environment:
	def __init__(self,screen_title,screen_width=640,screen_height=480):
		init()
		key.set_repeat(1,1)
		self.last_sprite_created = None
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.gameScreen = GameScreen(self.screen_width,self.screen_height)
		self.sprite_buffer_xpos = 0
		self.sprite_buffer_ypos = 2000
		self.max_frame = 60
		self.coll_detect = 1
		self.backdrop_on = 0
		self.backdrop_image = ""
		self.screen_title = screen_title
		display.set_caption(self.screen_title)
		self.currentGameTimer = GameTimer(self)
		self.currentScore = GameScore(self)

	def next_sprite_buffer_slot(self):
		#global sprite_buffer_xpos,sprite_buffer_ypos
		last_sprite_frame_assigned = int(self.last_sprite_created.currentSpriteFrame)
		last_sprite_width = self.last_sprite_created.sprite_frame[last_sprite_frame_assigned][1]
		last_sprite_height = self.last_sprite_created.sprite_frame[last_sprite_frame_assigned][2]
	
		if ( self.sprite_buffer_xpos + last_sprite_width ) \
			> (self.screen_height * 0.9 ):
			self.sprite_buffer_ypos += last_sprite_height
			self.sprite_buffer_xpos = 0
		else:
			self.sprite_buffer_xpos += last_sprite_width		
		
	def set_collision_detect(self,coll_detect=1):
		if coll_detect == 0:
			self.coll_detect = 0
		else:
			self.coll_detect = 1
	
	def set_backdrop(self,backdrop_image):
		self.backdrop_image = image.load(backdrop_image)
	
	def draw_backdrop(self):
		if self.backdrop_on:
			self.gameScreen.screen.blit(self.backdrop_image, (0,0))
		else:
			self.gameScreen.screen.fill((0,0,0))
			
	def backdrop_status(self,backdrop_on):
		if backdrop_on == 0:
			self.backdrop_on = 0
		else:
			self.backdrop_on = 1			

	def setTitle(self,newTitle):
		self.screen_title = newTitle
		display.set_caption(self.screen_title)
		
	def setSpriteBufferLocation(self,sb_x,sb_y):
		self.sprite_buffer_xpos = sb_x
		self.sprite_buffer_ypos = sb_y
	
	def setScreenDimensions(self,scr_x,scr_y):
		self.screen_width = scr_x
		self.screen_height = scr_y
		gameScreen.screen = display.set_mode((self.screen_width,self.screen_height))
		
	
class GameScreen:
	def __init__(self,screen_width,screen_height):
		self.screen = display.set_mode((screen_width,screen_height))
		
	def returnScreenObject(self):
		return self.screen
	
		
def collision_detect(gameEnv, sprite1_xpos,sprite1_ypos,sprite2_xpos,sprite2_ypos,\
		sprite2_width,sprite2_height):

	if (sprite1_xpos > (sprite2_xpos - sprite2_width) ) and \
	(sprite1_xpos < ( sprite2_xpos + sprite2_width ) ) and \
	(sprite1_ypos > (sprite2_ypos - sprite2_height ) ) and \
	(sprite1_ypos < (sprite2_ypos + sprite2_height ) ):
		if gameEnv.coll_detect == 1:
			return 1
		else:
			return 0
	else:
		return 0
		
