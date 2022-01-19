import pygame

from defs import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_pos, x, y, value, first = False):
        super().__init__()

        self.size = TILE_SIZE
        self.image = pygame.Surface((self.size,  self.size))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.grid_pos = grid_pos

        self.rect.center = (x+TILE_SIZE/2,y+TILE_SIZE/2)
        self.x = x
        self.y = y

        self.dir = pygame.Vector2(0,0)

        self.value = value
        
        self.spawn = first
        if self.spawn:
            self.size = TILE_SIZE / 10
            self.image = pygame.Surface((self.size,  self.size))
            self.image.fill((255, 255, 0))

    def spawn_anim(self):
        if self.image.get_size()[0] == TILE_SIZE:
            self.spawn = False
        else:
            self.size += TILE_SIZE / 10
            self.image = pygame.Surface((self.size,  self.size))
            self.image.fill((255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x+TILE_SIZE/2,self.y+TILE_SIZE/2)

    def display_num(self, display, font):
        text = font.render(f'{self.value}', 1, FONT_COLOR)
        display.blit(text, self.rect.midtop)
    
    def set_animation_dir(self, dir):
        self.dir.x = dir[0]
        self.dir.y = dir[1]
        print(self.dir)

    def animate(self):
        self.rect.x += self.dir.x * TILE_ANIM_SPEED
        self.rect.y += self.dir.y * TILE_ANIM_SPEED

    def update(self, display, font):
        self.display_num(display, font)
        if self.spawn:
            self.spawn_anim()