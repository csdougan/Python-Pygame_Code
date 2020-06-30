import pygame
# Global constants
# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
    # -- Methods
    def __init__(self):
        """ Constructor function """
        # Call the parent's constructor
        super(Player,self).__init__()
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        # List of sprites we can bump against
        self.level = None
    def update(self):
        """ Move the player. """
        # Move left/right
        self.rect.x += self.change_x
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    # How far this world has been scrolled left/right
    world_shift = 0
    square_list = []
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.player = player
        self.backgroundCanvas = pygame.Surface([SCREEN_WIDTH*2, SCREEN_HEIGHT])
        self.backgroundCanvas.fill(BLACK)
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
    def draw(self, screen):
        """ Draw everything on this level. """
        # Draw the background
        screen.fill(BLACK)
        #draw squares on background canvas
        #pygame.draw.rect(self.backgroundCanvas,(50,50,50),[100,400,150,SCREEN_HEIGHT])
                               
        for i in range(len(self.square_list)):
                                                pygame.draw.rect(self.backgroundCanvas,(50,50,50),self.square_list[i])
                               
                                #copy section of background canvas that is visible to 'screen' surface
        screen.blit(self.backgroundCanvas,(0+self.world_shift,0))
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """
        # Keep track of the shift amount
        self.world_shift -= shift_x
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
    def __init__(self, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = 230
        # Array with width, height, x, and y of platform
        self.square_list.append([100, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([200, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([300, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([400, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([500, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([600, 400, 50, SCREEN_HEIGHT-400])
        self.square_list.append([700, 400, 50, SCREEN_HEIGHT-400])
        #self.square_list.append([800, 400, 50, SCREEN_HEIGHT-400])
        #self.square_list.append([900, 400, 50, SCREEN_HEIGHT-400])
        #self.square_list.append([1000, 400, 50, SCREEN_HEIGHT-400])
        #self.square_list.append([1100, 400, 50, SCREEN_HEIGHT-400])
                
 
 
        # Go through the array above and add platforms
        #for platform in level:
            #block = Platform(platform[0], platform[1])
            #block.rect.x = platform[2]
            #block.rect.y = platform[3]
            #block.player = self.player
           # self.platform_list.add(block)
 
def main():
    """ Main Program """
    pygame.init()
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("")
    # Create the player
    player = Player()
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------
    left_scroll_boundary=120
    right_scroll_boundary=500
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        # Update the player.
        active_sprite_list.update()
        # Update items in the level
        current_level.update()
        if player.rect.right > right_scroll_boundary:
                                                #distance_to_scroll is how many pixels over the right scroll boundary the player goes
                                                distance_to_scroll = player.rect.right - right_scroll_boundary
                                                #once the distance to scroll is worked out, the player is moved back to the right boundary
                                                player.rect.right = right_scroll_boundary
                                               
                                                # If the player gets to the end of the level, dont move any further
                                                current_position = player.rect.x + current_level.world_shift
                                                if current_position < current_level.level_limit:
                                                                player.rect.x = int(current_level.level_limit) - current_level.world_shift
                                                else:
                                                                current_level.shift_world(distance_to_scroll)
 
  
  
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= left_scroll_boundary:
            diff = left_scroll_boundary - player.rect.left
            player.rect.left = left_scroll_boundary
            current_level.shift_world(-diff)
     
                                               
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
if __name__ == "__main__":
    main()