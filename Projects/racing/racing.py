from pygame import *
import random

global SpriteWidth, SpriteHeight
SpriteWidth, SpriteHeight = 40,40

class Sprite:
	def __init__(self, xpos, ypos, filename):
		self.x = xpos
		self.y = ypos
		self.bitmap = image.load(filename)
	def render(self):
		screen.blit(self.bitmap, (self.x,self.y))

class FlippedSprite(Sprite):
	def __init__(self,xpos,ypos,filename):
		Sprite.__init__(self,xpos,ypos,filename)
		self.bitmap = transform.flip(self.bitmap,False,True)
	

def collision_detect(s1_x,s1_y,s2_x,s2_y):
	if (s1_x > s2_x - SpriteWidth) and (s1_x < s2_x + SpriteWidth) and (s1_y > s2_y - SpriteHeight) and (s1_y < s2_y + SpriteHeight):
		return 1
	else:
		return 0


init()
screen = display.set_mode((640,480))
display.set_caption('Racing Game')
#mixer.music.load('data/background.mod')
#mixer.music.play(-1)

playercar = Sprite(200,400,'assets/car.png')
enemycar = FlippedSprite(random.randrange(100,500),0,'assets/car2.png')
tree1 = Sprite(10,0,'assets/tree.png')
tree2 = Sprite(550,240,'assets/tree.png')

whiteline1 = Sprite(315,0,'assets/whiteline.png')
whiteline2 = Sprite(315,240,'assets/whiteline.png')

scorefont = font.Font(None, 60)
#crasheffect = mixer.Sound('data/crash.wav')

score = 0
maxscore = 0
quit = 0
oldmousex,oldmousey=mouse.get_pos()
speed = 10
enemyspeed = 5
while quit == 0:
	screen.fill((0,200,0))
	screen.fill((200,200,200),((100,0),(440,480)))
	
	tree1.render()
	tree1.y += speed
	if (tree1.y > 480):
		tree1.y = -110
	tree2.render()
	tree2.y += speed
	if (tree2.y > 480):
		tree2.y = -110
	
	whiteline1.render()
	whiteline1.y += speed
	if (whiteline1.y > 480):
		whiteline1.y = -80
	whiteline2.render()
	whiteline2.y += speed
	if (whiteline2.y > 480):
		whiteline2.y = -80
	enemycar.y += (speed + enemyspeed)
	if (enemycar.y > 480):
		enemycar.y = -100
		enemycar.x = random.randrange(100,500)

	for userevent in event.get():
		if userevent.type == MOUSEBUTTONUP:
			None
		if userevent.type == QUIT:
			quit = 1

	mousex,mousey = mouse.get_pos()
	if (mousex < 100):
		mousex = 100
	if (mousex > 500):
		mousex = 500
	if (mousey < oldmousey) and (speed <= 30):
		speed +=5 
	if (mousey > (oldmousey+20)) and (speed != 0):
		speed -=5 
	oldmousey = mousey

	playercar.x = mousex

	scoretext = scorefont.render('Score: ' + str(score), True, (255,255,255), (0,0,0))
	screen.blit(scoretext, (5,5))
	
	if (collision_detect(playercar.x,playercar.y,enemycar.x,enemycar.y)):
		speed = 0
		enemyspeed = 0
		score = 0
		time.delay(100)
		enemycar.y = -100
		enemycar.x = random.randrange(100,500)
		#playercar.render()
		#enemycar.render()
		#display.update()
		time.delay(500)
	speed = 10
	enemyspeed = 5
	enemycar.render()
	playercar.render()

	score += 1
	time.delay(50)
	display.update()

