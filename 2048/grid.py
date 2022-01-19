from turtle import update
import pygame
from scipy import rand
from defs import *
from tile import Tile
import random

class Grid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 255, 240))
        self.rect = self.image.get_rect(center = (WIDTH/2, (HEIGHT/2 + TOP_PLUS_OFFSET))) 

        self.tile_poses = [[((LEFT_OFFSET + TILE_GAP, TOP_OFFSET + TILE_GAP)),((LEFT_OFFSET + (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP)),((LEFT_OFFSET + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP)),((LEFT_OFFSET + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP))],
                          [((LEFT_OFFSET + TILE_GAP, TOP_OFFSET + TILE_GAP+ (TILE_SIZE + TILE_GAP))),((LEFT_OFFSET + (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP))),((LEFT_OFFSET + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP))),((LEFT_OFFSET + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)))],
                          [((LEFT_OFFSET + TILE_GAP, TOP_OFFSET + TILE_GAP+ (TILE_SIZE + TILE_GAP)*2)),((LEFT_OFFSET + (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*2)),((LEFT_OFFSET + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*2)),((LEFT_OFFSET + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*2))],
                          [((LEFT_OFFSET + TILE_GAP, TOP_OFFSET + TILE_GAP+ (TILE_SIZE + TILE_GAP)*3)),((LEFT_OFFSET + (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*3)),((LEFT_OFFSET + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*3)),((LEFT_OFFSET + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, TOP_OFFSET + TILE_GAP + (TILE_SIZE + TILE_GAP)*3))]]

        self.tiles = pygame.sprite.Group()
        self.tile_data = [[0,0,0,0],
                          [0,0,0,0],
                          [0,0,0,0],
                          [0,0,2,0]]
        self.set_tiles()

        self.keys_pressed = {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        
        
        #self.test_all()

    def test_all(self):
        for row in self.tile_poses:
            for cell in row:
                kohta = cell
                self.tiles.add(Tile(kohta[0], kohta[1]))

    def set_tiles(self):
        self.tiles.empty()
        for row_i, row  in enumerate(self.tile_data):
            for col_i, cell in enumerate(row):
                kohta = self.tile_poses[row_i][col_i]
                if(cell != 0):
                    self.tiles.add(Tile(kohta[0], kohta[1], cell))
    def create_tile_animation(self, x, y, des_x, des_y):
        pass
                
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.keys_pressed[pygame.K_RIGHT] == False:
            self.keys_pressed[pygame.K_RIGHT] = True
            self.move((1,0))
        else:
            if not keys[pygame.K_RIGHT]:
                self.keys_pressed[pygame.K_RIGHT] = False
            if keys[pygame.K_LEFT] and self.keys_pressed[pygame.K_LEFT] == False:
                self.keys_pressed[pygame.K_LEFT] = True
                self.move((-1,0))
            else:
                if not keys[pygame.K_LEFT]:
                    self.keys_pressed[pygame.K_LEFT] = False
                if keys[pygame.K_UP] and self.keys_pressed[pygame.K_UP] == False:
                    self.keys_pressed[pygame.K_UP] = True
                    self.move((0,-1))
                else:
                    if not keys[pygame.K_UP]:
                        self.keys_pressed[pygame.K_UP] = False
                    if keys[pygame.K_DOWN] and self.keys_pressed[pygame.K_DOWN] == False:
                        self.keys_pressed[pygame.K_DOWN] = True
                        self.move((0,1))
                    elif not keys[pygame.K_DOWN]:
                        self.keys_pressed[pygame.K_DOWN] = False

    
    def move(self, dir: tuple):
        if dir[0] != 0: #horizontal
            if dir[0] == 1:
                for row in range(0, 4, 1):
                    max = 3
                    for col in range(2, -1, -1):
                        tile = self.tile_data[row][col]
                        if tile != 0:
                            self.tile_data[row][col] = 0
                            while self.tile_data[row][max] != 0 and self.tile_data[row][max] != tile:
                                max -= 1
                                if max == 0:
                                    break
                            if tile == self.tile_data[row][max]:
                                self.tile_data[row][max] = tile * 2
                                max -= 1
                            else:
                                self.tile_data[row][max] = tile
            else:  
                for row in range(0, 4, 1):
                    min = 0
                    for col in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        if tile != 0: 
                            self.tile_data[row][col] = 0
                            while self.tile_data[row][min] != 0 and self.tile_data[row][min] != tile:
                                min += 1
                                if min == 3:
                                    break
                            if tile == self.tile_data[row][min]:
                                self.tile_data[row][min] = tile * 2
                                min += 1 
                            else:
                                self.tile_data[row][min] = tile
        else: #vertical
            if dir[1] == 1:
                for col in range(0, 4, 1):
                    max = 3
                    for row in range(2, -1, -1):
                        tile = self.tile_data[row][col]
                        if tile != 0:     
                            self.tile_data[row][col] = 0
                            while self.tile_data[max][col] != 0 and self.tile_data[max][col] != tile:
                                max -= 1
                                if max == 0:
                                    break
                            if tile == self.tile_data[max][col]:     
                                self.tile_data[max][col] = tile * 2
                                max -= 1
                            else:
                                self.tile_data[max][col] = tile
            else:
                for col in range(0, 4, 1):
                    min = 0
                    for row in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        if tile != 0:
                            self.tile_data[row][col] = 0
                            while self.tile_data[min][col] != 0 and self.tile_data[min][col] != tile:
                                min += 1
                                if min == 3:
                                    break
                            if tile == self.tile_data[min][col]:
                                self.tile_data[min][col] = tile * 2
                                min += 1
                            else:
                                self.tile_data[min][col] = tile


        kohta = (random.randint(0, 3), random.randint(0, 3))
        lista = [(0,0),(0,1),(0,2),(0,3),
                (1,0),(1,1),(1,2),(1,3),
                (2,0),(2,1),(2,2),(2,3),
                (3,0),(3,1),(3,2),(3,3)]
        while self.tile_data[kohta[0]][kohta[1]] != 0 and lista:
            #print(kohta)
            lista.remove(kohta)
            if not lista:
                self.game_over()
            else:
                kohta = random.choice(lista)

        if lista:
            self.tile_data[kohta[0]][kohta[1]] = 2

        self.animate_tiles()
        #self.set_tiles()
    
    def game_over(self):
        print('Huono')
    
    def animate_tiles(self):
        pass

    def update(self, display, font):
        self.tiles.draw(display)
        self.get_input()
        self.tiles.update(display, font)
    