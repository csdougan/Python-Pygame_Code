from pygame import *
import random

tiles_across,tiles_down = 3,3
BLACK=(0,0,0)

class Tile:
	def __init__(self,pos):
		self.actualpos = pos
		self.correctpos = pos
	def render(self):
		ya = self.actualpos / tiles_down 
		xa = self.actualpos % tiles_across 

		yc = self.correctpos / tiles_down
		xc = self.correctpos % tiles_across
		self.tile_height = (mainpic.get_height() / tiles_down) 
		self.tile_width = (mainpic.get_width() / tiles_across)

		if self.correctpos != 8:

			screen.blit(mainpic, [xa*self.tile_width,ya*self.tile_height,self.tile_width,self.tile_height],[xc*self.tile_width,yc*self.tile_height,self.tile_width,self.tile_height])

'''		0 1 2
		3 4 5
		6 7 8
'''
def swap_tile(num):
	tile_to_left = (num - 1)
	if (tile_to_left < 0):
		tile_to_left = -1
	
	tile_to_right = num + 1
	if (tile_to_right % tiles_across) == 0:
		tile_to_right = -1
	
	tile_above = num - tiles_across
	if (tile_above < 0):
		tile_above = -1

	tile_below = num + tiles_across
	if (tile_below >= (tiles_across * tiles_down)):
		tile_below = -1
	
	try_swap(num,tile_to_left,tile_to_right,tile_above,tile_below)

	
# return number of tile at current position
def find_pos(pos):
	for x in range(9):
		if tile_list[x].actualpos == pos:
			return x
	return -1


# swap positions of two tiles
def swap_pos(one,two):
	tmp = tile_list[one].actualpos
	tile_list[one].actualpos = tile_list[two].actualpos
	tile_list[two].actualpos = tmp

def try_swap(clicked,pos1,pos2,pos3,pos4):
	num = find_pos(clicked)
	a = find_pos(pos1)
	b = find_pos(pos2)
	c = find_pos(pos3)
	d = find_pos(pos4)

	if a != -1 and tile_list[a].correctpos == 8:
		swap_pos(a,num)
		return
	if b != -1 and tile_list[b].correctpos == 8:
		swap_pos(b,num)
		return
	if c != -1 and tile_list[c].correctpos == 8:
		swap_pos(c,num)
		return
	if d != -1 and tile_list[d].correctpos == 8:
		swap_pos(d,num)
		return


init()
screen = display.set_mode((480,480))
display.set_caption('Shuffle')
mainpic = image.load('assets/earth.jpg')
highlight = image.load('assets/highlight.png')
hl_w=highlight.get_width()
hl_h=highlight.get_height()

player_tile, quit = 0, 0

tile_list=[]
for x in range(9):
	tmp_tile = Tile(x)
	tile_list.append(tmp_tile)

for x in range(1000):
	swap_tile(random.randrange(0,8))


while quit == 0:
	screen.fill(BLACK)

	for x in range(9):
		tile_list[x].render()

	highlight_x = ( player_tile % tiles_across ) * ( tile_list[player_tile].tile_width )
	highlight_y = ( player_tile / tiles_down ) * ( tile_list[player_tile].tile_height )
	screen.blit(highlight, (highlight_x, highlight_y))
	display.update()

	userinput = event.wait()
	if userinput.type == QUIT:
		quit = 1

	if userinput.type == KEYDOWN:

		if userinput.key == K_UP:
			if (player_tile - tiles_across) >= 0:
				player_tile -= tiles_across

		if userinput.key == K_DOWN:
			if (player_tile + tiles_across) < (tiles_across * tiles_down):
				player_tile += tiles_across
		if userinput.key == K_LEFT:
			if (player_tile % 3) != 0:
				player_tile -= 1

		if userinput.key == K_RIGHT:
			if (((player_tile + 1) % 3) != 0):
				player_tile += 1

		if userinput.key == K_SPACE:
			swap_tile(player_tile)

		if userinput.key == K_ESCAPE:
			quit = 1

success = 1
for x in range(9):
	if tile_list[x].actualpos != tile_list[x].correctpos:
		success = 0

if success == 1:
	print "congratulations, you did it"
else:
	print "too bad"

