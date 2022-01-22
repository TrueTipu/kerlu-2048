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


    def display_text(self,text: str, display, color):
        font = pygame.font.SysFont("comic sans", FONT_SIZE_1 - (len(text)-1)* 14)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center = self.rect.center)
        display.blit(text_surf, (text_rect.x, text_rect.y))
    
    def set_animation_dir(self, dir):
        self.dir.x = dir[0]
        self.dir.y = dir[1]
        #print(self.dir)

    def animate(self):
        self.rect.x += self.dir.x * TILE_ANIM_SPEED
        self.rect.y += self.dir.y * TILE_ANIM_SPEED

    def update(self, display):
        if self.spawn:
            self.spawn_anim()
        else:
            self.display_text(str(self.value),display, (0,0,0))