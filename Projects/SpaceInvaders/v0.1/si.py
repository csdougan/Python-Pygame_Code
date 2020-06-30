from pygame import *
from lib import TwoDee
#from TwoDee import Game_Environment,relocate_sprite, GameScreen, Sprite,collision_detect, move_sprite, relocate_sprite, GameTimer, GameScore
import random, math

global ENEMY_SPEED, MOVE_DOWN
MOVE_DOWN=1
ENEMY_SPEED=1
			
def initialise_sprites():
	global backdrop,playerShip,playerMissile,enemyMissile, enemies
	
	playerShip = TwoDee.Sprite(gameEnv,'assets/Ship.png','assets/Ship.png')
	playerMissile = TwoDee.Sprite(gameEnv,'assets/missile.png')
	enemyMissile = TwoDee.Sprite(gameEnv,'assets/missile.png')
	enemies = []
	x = 0
	for i in range(10):
		enemies.append(TwoDee.Sprite(gameEnv,'assets/InvaderA_00.png', 'assets/InvaderA_01.png'))
	for i in range(10,20):
		enemies.append(TwoDee.Sprite(gameEnv,'assets/InvaderB_00.png', 'assets/InvaderB_01.png'))
		enemies[i].randomCurrentFrame(True)
	for i in range(20,30):
		enemies.append(TwoDee.Sprite(gameEnv,'assets/InvaderC_00.png', 'assets/InvaderC_01.png'))
				
def assign_starting_positions():
	TwoDee.relocate_sprite(playerShip,(gameEnv.screen_width / 2) - (playerShip.sprite_width / 2),400)
	for i in range(10):
		TwoDee.relocate_sprite(enemies[i],(50 * i) + 50,50)
	for i in range(10,20):
		TwoDee.relocate_sprite(enemies[i],(50 * (i-10)) + 50,100)
	for i in range(20,30):
		TwoDee.relocate_sprite(enemies[i],(50 * (i-20)) + 50,150)
		
		
def initial_setup():
	global gameEnv
	# Create a new game environment
	gameEnv = TwoDee.Game_Environment('Space Invaders')
	# Setup sprites - initially these will be set at a position off screen	
	initialise_sprites()
	# move sprites to their starting positions 
	assign_starting_positions()
	gameEnv.backdrop_status(1)
	gameEnv.set_backdrop('assets/Starfield.jpg')
	

def change_enemy_direction():
	global ENEMY_SPEED
	ENEMY_SPEED *= -1

def start_screen():
		global quit
		gameEnv.draw_backdrop()
		gameFont = font.SysFont("monospace", 34)
		pressText = ("Press any Key to Start")
		pressTextObj = gameFont.render(pressText, 1 ,(255,255,255))
		gameEnv.gameScreen.screen.blit(pressTextObj,((gameEnv.screen_width / 2) - (pressTextObj.get_width() /2),\
		(gameEnv.screen_height / 2) - (pressTextObj.get_height() /2)))

		display.update()
		time.delay(10)
		start_game = 0
		quit = 0
		while quit == 0 and start_game == 0:
			for userinput in event.get():
				if userinput.type == QUIT:
					quit = 1
				if userinput.type == KEYDOWN:
					start_game = 1		
		

def main_loop():
	global quit
		
	gameEnv.currentGameTimer.current_frame = 0
	while quit == 0:
		gameEnv.currentGameTimer.current_frame += 1
		if gameEnv.currentGameTimer.current_frame > gameEnv.max_frame:
			gameEnv.currentGameTimer.current_frame = 1
		last_enemy = (len(enemies) - 1)
		remaining_enemies = len(enemies)
		gameEnv.draw_backdrop()
		
		# move enemies 
		for i in range(remaining_enemies):
			TwoDee.move_sprite(enemies[i],ENEMY_SPEED,0)
			enemies[i].render()
		
		# check if enemies have reached screen boundary 
		# if so then change their direction
		if (enemies[last_enemy].x > 590) or (enemies[0].x < 10):
			change_enemy_direction()
			if MOVE_DOWN == 1:
				for i in range(remaining_enemies):
					TwoDee.move_sprite(enemies[i],0,5)
					
		# check if player missile is in playing area
		if playerMissile.y < gameEnv.screen_height and playerMissile.y > 0:
			playerMissile.render()
			TwoDee.move_sprite(playerMissile,0,-5)
		
		# check if an enemy missile is in playing area.  If not
		# assign one to a random enemy
		if enemyMissile.y >= gameEnv.screen_height and remaining_enemies > 0:
			firing_enemy=(random.randrange(remaining_enemies))
			firing_enemy_xpos=enemies[firing_enemy].x
			firing_enemy_ypos=enemies[firing_enemy].y
			TwoDee.relocate_sprite(enemyMissile,firing_enemy_xpos,firing_enemy_ypos)
			
		
		# Look for successful hit by enemy missile
		if TwoDee.collision_detect\
		(gameEnv, playerShip.x,playerShip.y,enemyMissile.x,enemyMissile.y,\
		enemyMissile.sprite_width,enemyMissile.sprite_height):
			quit = 1
		
		# Look for successful hit by player missile
		for i in range(0, remaining_enemies):
			if TwoDee.collision_detect(gameEnv, playerMissile.x, playerMissile.y, \
			enemies[i].x, enemies[i].y, enemies[i].sprite_width,\
			enemies[i].sprite_height):
				gameEnv.currentScore.increase_score(50)
				del enemies[i]
				#relocate_sprite(playerMissile,playerMissile.buffer_x,playerMissile.buffer_y)
				TwoDee.relocate_sprite(playerMissile,playerMissile.sprite_frame[0][3],playerMissile.sprite_frame[0][4])
				break
		if remaining_enemies == 0:
			quit = 1
			
		for userinput in event.get():
			if userinput.type == QUIT:
				quit = 1
			if userinput.type == KEYDOWN:
				if userinput.key == K_RIGHT and playerShip.x < 590:
					TwoDee.move_sprite(playerShip,5,0)
				if userinput.key == K_LEFT and playerShip.x > 10:
					TwoDee.move_sprite(playerShip,-5,0)
				if userinput.key == K_SPACE:
					missile_x = playerShip.x + ((playerShip.sprite_width / 2) - (playerMissile.sprite_width / 2))
					TwoDee.relocate_sprite(playerMissile,missile_x,playerShip.y)
				if userinput.key == K_q:
					quit = 1
				if userinput.key == K_p:
					pause_game = 1
					while pause_game == 1:
						for pauseinput in event.get():
							if pauseinput.type == KEYDOWN:
								if pauseinput.key == K_ESCAPE:
									pause_game = 0
									time.delay(20)
						time.delay(20)
		
		TwoDee.move_sprite(enemyMissile,0,5)
		gameEnv.currentScore.render()
		gameEnv.currentGameTimer.render()
		enemyMissile.render()
		playerShip.render()
		display.update()
		time.delay(10)
				

initial_setup()
start_screen()
main_loop()

