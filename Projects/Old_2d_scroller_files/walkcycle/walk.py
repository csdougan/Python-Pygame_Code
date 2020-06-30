import pygame, sys, glob
from pygame import *

h=400
w=800
BLACK=(0,0,0)
FPS=60
pygame.init()
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

class player:
	def __init__(self):
		self.facingLeft = True
		self.x = 200
		self.y = 100
		self.ani_speed_init=5
		self.ani_speed=self.ani_speed_init
		self.ani = glob.glob("droid_walk*.png")
		self.ani.sort()
		self.ani_pos=0 
		self.ani_max = len(self.ani) - 1
		self.image_array_left = []
		self.image_array_right = []
		counter=0
		for imagename in self.ani:
			self.image_array_left.append(pygame.image.load(self.ani[counter]))
			self.image_array_right.append(pygame.transform.flip(self.image_array_left[counter], True, False))			
			counter += 1
		self.img = self.image_array_left[0]
		self.update(0)
	def update(self,pos):
		if pos != 0:
			self.ani_speed -= 1
			self.x += (pos * 2)
			if self.ani_speed == 0:
				if facingLeft:
					self.img = self.image_array_left[self.ani_pos]
				else:
					self.img = self.image_array_right[self.ani_pos]
				self.ani_speed = self.ani_speed_init
				if self.ani_pos == self.ani_max:
					self.ani_pos = 0
				else:
					self.ani_pos += 1
		screen.blit(self.img,(self.x,self.y))

player1 = player()
pos = 0
	
while True:
	screen.fill(BLACK)
	clock.tick(FPS)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == KEYDOWN and event.key == K_RIGHT:
			pos = 1
			facingLeft = False
		elif event.type == KEYUP and event.key == K_RIGHT:
			pos = 0
		elif event.type == KEYDOWN and event.key == K_LEFT:
			pos = -1
			facingLeft = True
		elif event.type == KEYUP and event.key == K_LEFT:
			pos = 0	
	
	player1.update(pos)
	pygame.display.flip()
