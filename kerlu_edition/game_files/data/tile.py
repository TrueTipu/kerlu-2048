import pygame
from math import log2

from data.defs import *

#sprite class jokaiselle yksittäiselle ruudulle jossa on numero, ei hallitse kovin paljoa sillä suurin osa logiikasta hoituu gridin kautta
class Tile(pygame.sprite.Sprite):

    def __init__(self, grid_pos, x, y, value, first = False): #init luodessa
        super().__init__() #kutsuu sprite inittiä että sprite toimii
        
        #luo muoto ja väri
        self.size = TILE_SIZE 
        self.path = TILE_ART_START+str(round(log2(value)))+TILE_ART_END
        self.image = pygame.image.load(self.path) #etsi oikean numeron art

        #aseta positio ja rectangle
        self.rect = self.image.get_rect()
        self.grid_pos = grid_pos
        self.rect.center = (x+TILE_SIZE/2,y+TILE_SIZE/2)
        self.x = x
        self.y = y

        #liikkumista varten vector 2 suunta
        self.dir = pygame.Vector2(0,0)

        #asetetaan arvo numero
        self.value = value
        
        #jos täysin tyhjästä syntynyt niin synny pienenä
        self.spawn = first
        if self.spawn:
            self.size = TILE_SIZE / 10
            self.image = pygame.transform.scale(self.image, (self.size, self.size))


    def spawn_anim(self): #kasva pienestä isoksi jos spawn statessa vielä
        if self.image.get_size()[0] == TILE_SIZE: #jos täysikokoinen niin lopeta kasvu
            self.image = pygame.image.load(self.path) #asettaa kuvan varmuudeksi uudestaan
            self.spawn = False
        else: #muuten kasva
            self.size += TILE_SIZE / 10 #kasvaa 10 osan koostaan
            #uudelleen scalee kuvaan ja asettaa ulkoasumuuttujansa uusiksi
            self.image = pygame.transform.scale(self.image, (self.size, self.size)) 
            self.rect = self.image.get_rect()
            self.rect.center = (self.x+TILE_SIZE/2,self.y+TILE_SIZE/2)
    
    def set_animation_dir(self, dir): #aseta liikkumasuunta halutuksi, grid scriptin kutsuma
        self.dir.x = dir[0]
        self.dir.y = dir[1]

    def animate(self): #liikuta haluttuun suuntaan nopeuden verran
        self.rect.x += self.dir.x
        self.rect.y += self.dir.y 


    def update(self): #grid kutsuu tätä joka frame pitääkseen ruudun ajan tasalla
        if self.spawn: #jos spawn statessa
            self.spawn_anim() #kutsu kasvatusta