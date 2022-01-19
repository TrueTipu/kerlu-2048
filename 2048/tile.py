import pygame

from defs import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (x,y)

        self.value = value
    def display_num(self, display, font):
        text = font.render(f'{self.value}', 1, FONT_COLOR)
        display.blit(text, self.rect.midtop)

    def update(self, display, font):
        self.display_num(display, font)
        