import pygame
from defs import *
from tile import Tile
from save_manager import Save_Manager
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

        self.tile_data = Grid.randomize_grid()

        self.set_tiles()

        self.score = 0
        self.high_score = Save_Manager.load()

        self.animation_on = False
        self.animation_count = 0

        self.keys_pressed = {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False}

        self.game_over_state = False

    def randomize_grid():
        first_1 = random.randint(0,15)
        first_2 = random.randint(0,15)
        if first_2 == first_1: first_2 += 1
        data =     [[0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]
        i = 0
        for row in data:
            for col_i in range(len(row)):
                i += 1
                if i == first_1 or i == first_2:
                    row[col_i] = 2
        return data


    def get_score(self):
        return self.score
    
    def get_high_score(self):
        return self.high_score

    def test_all(self):
        for row in self.tile_poses:
            for cell in row:
                kohta = cell
                self.tiles.add(Tile((row, cell), kohta[0], kohta[1]))

    def set_tiles(self):
        self.tiles.empty()
        for row_i, row  in enumerate(self.tile_data):
            for col_i, cell in enumerate(row):
                kohta = self.tile_poses[row_i][col_i]
                if(cell != 0):
                    if (cell == 1):
                        row[col_i] = 2
                        self.tiles.add(Tile((row_i, col_i),kohta[0], kohta[1], 2, True))
                    elif (cell == 3):
                        row[col_i] = 4
                        self.tiles.add(Tile((row_i, col_i),kohta[0], kohta[1], 4, True))
                    else:self.tiles.add(Tile((row_i, col_i),kohta[0], kohta[1], cell))
   
    def create_tile_animation(self, _row, _col, des_row, des_col, _dir):
        pos = self.tile_poses[_row][_col]
        des = self.tile_poses[des_row][des_col]

        dir = [0,0]
        if des[0] != pos[0]:
            speed =  abs(des[0] - pos[0]) / TILE_ANIM_LENGTH
            dir[0] = speed * _dir
        elif des[1] != pos[1]:
            speed =  abs(des[1] - pos[1]) / TILE_ANIM_LENGTH
            dir[1] = speed * _dir
        
        tile = next((x for x in self.tiles.sprites() if x.grid_pos == (_row, _col)), None)
        if tile:
            tile.set_animation_dir(dir)
        else:
            print('error?')
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        '''if keys[pygame.K_w]: print(self.neighbors(self.tile_data[0][0],0,0))
        if keys[pygame.K_e]: print(self.neighbors(self.tile_data[0][1],0,1))
        if keys[pygame.K_r]: print(self.neighbors(self.tile_data[0][2],0,2))
        if keys[pygame.K_t]: print(self.neighbors(self.tile_data[0][3],0,3))
        if keys[pygame.K_y]: print(self.neighbors(self.tile_data[1][0],1,0))
        if keys[pygame.K_u]: print(self.neighbors(self.tile_data[1][1],1,1))
        if keys[pygame.K_i]: print(self.neighbors(self.tile_data[1][2],1,2))
        if keys[pygame.K_o]: print(self.neighbors(self.tile_data[1][3],1,3))
        if keys[pygame.K_p]: print(self.neighbors(self.tile_data[2][0],2,0))
        if keys[pygame.K_a]: print(self.neighbors(self.tile_data[2][1],2,1))
        if keys[pygame.K_s]: print(self.neighbors(self.tile_data[2][2],2,2))
        if keys[pygame.K_d]: print(self.neighbors(self.tile_data[2][3],2,3))
        if keys[pygame.K_f]: print(self.neighbors(self.tile_data[3][0],3,0))
        if keys[pygame.K_g]: print(self.neighbors(self.tile_data[3][1],3,1))
        if keys[pygame.K_h]: print(self.neighbors(self.tile_data[3][2],3,2))
        if keys[pygame.K_j]: print(self.neighbors(self.tile_data[3][3],3,3)) '''

        if keys[pygame.K_RIGHT] and self.keys_pressed[pygame.K_RIGHT] == False:
            self.keys_pressed[pygame.K_RIGHT] = True
            self.move_manager((1,0))
        else:
            if not keys[pygame.K_RIGHT]:
                self.keys_pressed[pygame.K_RIGHT] = False
            if keys[pygame.K_LEFT] and self.keys_pressed[pygame.K_LEFT] == False:
                self.keys_pressed[pygame.K_LEFT] = True
                self.move_manager((-1,0))
            else:
                if not keys[pygame.K_LEFT]:
                    self.keys_pressed[pygame.K_LEFT] = False
                if keys[pygame.K_UP] and self.keys_pressed[pygame.K_UP] == False:
                    self.keys_pressed[pygame.K_UP] = True
                    self.move_manager((0,-1))
                else:
                    if not keys[pygame.K_UP]:
                        self.keys_pressed[pygame.K_UP] = False
                    if keys[pygame.K_DOWN] and self.keys_pressed[pygame.K_DOWN] == False:
                        self.keys_pressed[pygame.K_DOWN] = True
                        self.move_manager((0,1))
                    elif not keys[pygame.K_DOWN]:
                        self.keys_pressed[pygame.K_DOWN] = False

    def check_tile(self, _tile, _row, _col, _max, _min, max_dir, reverse = False)-> int:
        if _tile != 0: #jos liikutettava
            self.tile_data[_row][_col] = 0 #siirretään
            target_tile = self.tile_data[_row if not reverse else _max][_max if not reverse else _col] #asetetaan kohde maksimiin
            while target_tile != 0 and target_tile != _tile and _max != _min: #etsitään tyhjä tai sama tile
                _max += max_dir #lisätään maksimia
                target_tile = self.tile_data[_row if not reverse else _max][_max if not reverse else _col] #uudelleen asetetaan target

            if ((_row == _max and reverse) or (_col == _max and not reverse)):
                self.tile_data[_row][_col] = _tile
                return _max, False

            if _tile == target_tile: #jos sama
                self.tile_data[_row if not reverse else _max][_max if not reverse else _col] = _tile * 2 #asetetaan kaksinkertainen arvo
                if _tile * 2 == 2048:
                    self.voitto()
                self.score += _tile * 2
                self.create_tile_animation(_row, _col,_row if not reverse else _max,_max if not reverse else _col, max_dir*-1)
                _max += max_dir #lisää maxia ettei kaksi yhdisty samal kerral
            else:
                self.tile_data[_row if not reverse else _max][_max if not reverse else _col] = _tile
                self.create_tile_animation(_row, _col,_row if not reverse else _max,_max if not reverse else _col, max_dir*-1)

            return _max, True
        return _max, False
            
    def move_manager(self, dir: tuple):
        moved = False
        moved_vali = False
        if dir[0] != 0: #horizontal
            if dir[0] == 1:
                for row in range(0, 4, 1):
                    max = 3
                    for col in range(2, -1, -1):
                        tile = self.tile_data[row][col]
                        max, moved_vali = self.check_tile(tile, row, col, max, 0, -1)
                        if moved_vali:
                            moved = True
            else:  
                for row in range(0, 4, 1):
                    min = 0
                    for col in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        min, moved_vali = self.check_tile(tile, row, col, min, 3, 1)
                        if moved_vali:
                            moved = True
        else: #vertical
            if dir[1] == 1:
                for col in range(0, 4, 1):
                    max = 3
                    for row in range(2, -1, -1):
                        tile = self.tile_data[row][col]
                        max, moved_vali = self.check_tile(tile, row, col, max, 0, -1, True)
                        if moved_vali:
                            moved = True
            else:
                for col in range(0, 4, 1):
                    min = 0
                    for row in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        min,moved_vali = self.check_tile(tile, row, col, min, 3, 1, True)
                        if moved_vali:
                            moved = True

        if moved:   
            #uuden asettaminen             
            self.set_new_tile(True)
            self.animation_on = True
            self.animation_count = 0
        else:
            self.set_new_tile(False)
    
    def set_new_tile(self, set):
        kohta = (random.randint(0, 3), random.randint(0, 3))
        vapaat_paikat = [(0,0),(0,1),(0,2),(0,3),
                (1,0),(1,1),(1,2),(1,3),
                (2,0),(2,1),(2,2),(2,3),
                (3,0),(3,1),(3,2),(3,3)]

        while self.tile_data[kohta[0]][kohta[1]] != 0 and vapaat_paikat:

            vapaat_paikat.remove(kohta)
            if not vapaat_paikat:break

            kohta = random.choice(vapaat_paikat)
        

        if vapaat_paikat and set:
            self.tile_data[kohta[0]][kohta[1]] = random.choice((1,1,1,1,1,1,1,1,1,3))
        elif not vapaat_paikat:
            movable = False
            for row in range(len(self.tile_data)):
                    for col in  range(len(self.tile_data[0])):
                        if self.neighbors(self.tile_data[row][col], row, col):
                            #print(self.neighbors(self.tile_data[row][col], row, col))
                            movable = True
            if not movable: self.game_over()

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            Save_Manager.save(self.high_score)
        self.game_over_state = True
        #print('Huono')
    
    def voitto(self):
        print('Voitit')

    def animate_tiles(self):
        for tile in self.tiles.sprites():
            tile.animate()
        self.animation_on = False if self.animation_count >= TILE_ANIM_LENGTH else True
        self.animation_count += 1
        if not self.animation_on:
            self.set_tiles()
    
    def neighbors(self, _tile, row_number, column_number):
        a = self.tile_data
        lista = [a[i][j] 
            for i in range(row_number-1, row_number+2) 
                for j in range(column_number-1, column_number+2) 
                    if i > -1 and j > -1 and j < len(a[0]) and i < len(a) and (((i == row_number) or (j == column_number)) and not(j == column_number and i == row_number)) and a[i][j] == _tile]
        return lista
    
    def reset(self):
        self.game_over_state = False
        self.tile_data = Grid.randomize_grid()
        self.score = 0
        self.set_tiles()


    def update(self, display):
        self.tiles.draw(display)
        self.tiles.update(display)
        if self.animation_on:
            self.animate_tiles()
        else:
            self.get_input()
            