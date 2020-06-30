import pygame

from spritesheet_functions import SpriteSheet

class CollectCoin(pygame.sprite.Sprite):

    def __init__(self, sprite_name):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet(sprite_name + ".png")
	self.image = sprite_sheet.get_image(0,0,sprite_sheet.rect.width-1,sprite_sheet.rect.height-1)
        self.rect = self.image.get_rect()
