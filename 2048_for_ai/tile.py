import pygame
from math import log2

from defs import *

#sprite class jokaiselle yksittäiselle ruudulle jossa on numero, ei hallitse kovin paljoa sillä suurin osa logiikasta hoituu gridin kautta
class Tile(pygame.sprite.Sprite):

    def __init__(self, grid_pos, x, y, value, first = False): #init luodessa
        super().__init__() #kutsuu sprite inittiä että sprite toimii
        
        #luo muoto ja väri
        self.size = TILE_SIZE 
        self.image = pygame.Surface((self.size,  self.size))
        self.color = (255, 255 - (log2(value) - 1) * RED_VALUE, 0)#väri punaistuu jokaista generaatiota kohden
        self.image.fill(self.color) 

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
        #poistetaan tämäkin animaatio
        """   self.spawn = first
        if self.spawn:
            self.size = TILE_SIZE / 10
            self.image = pygame.Surface((self.size,  self.size))
            self.image.fill(self.color) """

        #turha
        """     def spawn_anim(self): #kasva pienestä isoksi jos spawn statessa vielä
        if self.image.get_size()[0] == TILE_SIZE: #jos täysikokoinen niin lopeta kasvu
            self.spawn = False
        else: #muuten kasva
            self.size += TILE_SIZE / 10 #kasvaa 10 osan koostaan
            #asettaa kaikki ulkoasumuuttujansa uusiksi
            self.image = pygame.Surface((self.size,  self.size))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x+TILE_SIZE/2,self.y+TILE_SIZE/2) """
    #turha
    """ 
    def display_text(self,text: str, display, color): #tekstin piirto koodi helpottamaan elämää kuten mainissa
        font = pygame.font.SysFont("comic sans", FONT_SIZE_1 - (len(text)-1)* 14) #määritä font tekstin pituuden mukaan
        #renderöi teksti ja piirrä se näytölle
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center = self.rect.center)
        display.blit(text_surf, (text_rect.x, text_rect.y)) """
    
    def set_animation_dir(self, dir): #aseta liikkumasuunta halutuksi, grid scriptin kutsuma
        self.dir.x = dir[0]
        self.dir.y = dir[1]

    def animate(self): #liikuta haluttuun suuntaan nopeuden verran
        self.rect.x += self.dir.x
        self.rect.y += self.dir.y 


    def update(self, display): #grid kutsuu tätä joka frame pitääkseen ruudun ajan tasalla
        #skipataan teksti koska resurssit
        pass#self.display_text(str(self.value),display, (0,0,0)) 