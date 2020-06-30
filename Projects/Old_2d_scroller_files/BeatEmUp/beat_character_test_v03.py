from pygame import *
from lib import TwoDee
import random, math

global DROID_SPEED
DROID_SPEED=-5

def initialise_sprites():
	global Actor, Droid
	Actor = TwoDee.Sprite(gameEnv,'assets/Actor_Run/actor_run01.png','assets/Actor_Run/actor_run02.png','assets/Actor_Run/actor_run03.png','assets/Actor_Run/actor_run04.png','assets/Actor_Run/actor_run05.png','assets/Actor_Run/actor_run06.png','assets/Actor_Run/actor_run07.png','assets/Actor_Run/actor_run08.png','assets/Actor_Stance/actor_stance_01.png','assets/Actor_Stance/actor_stance_02.png','assets/Actor_Stance/actor_stance_03.png','assets/Actor_Stance/actor_stance_04.png','assets/Actor_Stance/actor_stance_05.png','assets/Actor_Stance/actor_stance_06.png','assets/Actor_Stance/actor_stance_07.png','assets/Actor_Stance/actor_stance_08.png')
	Droid = TwoDee.Sprite(gameEnv,'assets/Droid_Walk/droid_walk_01.png','assets/Droid_Walk/droid_walk_02.png','assets/Droid_Walk/droid_walk_03.png','assets/Droid_Walk/droid_walk_04.png','assets/Droid_Walk/droid_walk_05.png','assets/Droid_Walk/droid_walk_06.png','assets/Droid_Walk/droid_walk_07.png','assets/Droid_Walk/droid_walk_08.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_01.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_02.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_03.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_04.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_05.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_06.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_07.png','assets/Droid_Walk_Head_Spin/droid_walk_spin_08.png')
	Actor.set_sprite_frame_range(8,15)
	Droid.set_sprite_frame_range(0,7)
	
def assign_starting_positions():
	TwoDee.relocate_sprite(Actor,300,300)
	TwoDee.relocate_sprite(Droid,100,50)
	
def initial_setup():
	global gameEnv
	gameEnv = TwoDee.Game_Environment('Beat Em Up Test')
	initialise_sprites()
	assign_starting_positions()
	gameEnv.backdrop_status(0)

class DroidSprite(Sprite):
	def __init__(self,gameEnv,*filename):
		Sprite.__init__(self, gameEnv,*filename)
def move_Droid():
		global DROID_SPEED, Droid, droidMaxCount, droidSpin,droidCount
		droidCount += 1
		if droidCount == droidMaxCount:
			droidCount = 0
			if droidSpin == False:
				droidMaxCount = Droid.totalSpritestoUse * 10
				Droid.set_sprite_frame_range(8,15)
				droidSpin = True
			else:
				droidMaxCount = Droid.totalSpritestoUse * 40
				Droid.set_sprite_frame_range(0,7)
				droidSpin = False
		if (Droid.x > ((gameEnv.screen_width - (Droid.sprite_width * 2))) or (Droid.x < Droid.sprite_width)):
			#change Droid direction
			DROID_SPEED *= -1
			Droid.flip_horizontal(-1)
		TwoDee.move_sprite(Droid,DROID_SPEED,0)
		
			
	
def main_loop():
	global quit, actorFacing, droidSpin,droidCount, droidMaxCount
	droidSpin=False
	droidCount=0
	droidMaxCount=Droid.totalSpritestoUse * 6
	quit = 0
	actorFacing="right"
	actorRunning=False
	
	gameEnv.currentGameTimer.current_frame = 0
	while quit == 0:
		gameEnv.currentGameTimer.current_frame += 1
		if gameEnv.currentGameTimer.current_frame > gameEnv.max_frame:
			gameEnv.currentGameTimer.current_frame = 1
		gameEnv.draw_backdrop()
		
		for userinput in event.get():
			if userinput.type == QUIT:
				quit == 1
			if userinput.type == KEYDOWN:
				Actor.set_sprite_frame_range(0,7)
				if userinput.key == K_q:
					quit = 1
				if userinput.key == K_LEFT:
					if actorFacing == "right":
						Actor.flip_horizontal()
						actorFacing = "left"
					TwoDee.move_sprite(Actor,-5,0)
				if userinput.key == K_RIGHT:
					if actorFacing == "left":
						Actor.flip_horizontal()
						actorFacing = "right"
					TwoDee.move_sprite(Actor,5,0)
			if userinput.type == KEYUP:
				Actor.set_sprite_frame_range(8,15)
		move_Droid()
		Actor.render()
		Droid.render()
		display.update()
		time.delay(25)
		

initial_setup()
main_loop()
		
		
	
	

