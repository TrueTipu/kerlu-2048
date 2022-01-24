from turtle import color
import pygame
from defs import *
from tile import Tile
from save_manager import Save_Manager
import random

#sprite class gridille (kuvana vain valkoinen tausta) joka myös hallitsee koko pelilogiikkaa
#spriten olisi voinut erottaa tästä mutta se olisi ollut turhaa joten pistin samaan
class Grid(pygame.sprite.Sprite):

    def __init__(self, x, y): #init luodessa
        super().__init__() #kutsuu sprite inittiä että sprite toimii¨

        #luo valkoisen kuvan ja asettelee sen rectanglen avulla (kaikki tämän jälkeen on pelkkää pelilogiikkaa)
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 255, 240))
        self.rect = self.image.get_rect(topleft = (x, y)) 

        #laskee jokaisen tilen pikselisijainnin ja tallentaa ne matriisiin myöhemmin kätettäviksi
        self.tile_poses = [[((x + TILE_GAP, y + TILE_GAP)),((x + (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP)),((x + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP)),((x + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP))],
                          [((x + TILE_GAP, y + TILE_GAP+ (TILE_SIZE + TILE_GAP))),((x + (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP))),((x + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP))),((x + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)))],
                          [((x + TILE_GAP, y + TILE_GAP+ (TILE_SIZE + TILE_GAP)*2)),((x + (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*2)),((x + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*2)),((x + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*2))],
                          [((x + TILE_GAP, y + TILE_GAP+ (TILE_SIZE + TILE_GAP)*3)),((x + (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*3)),((x + 2 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*3)),((x + 3 * (TILE_SIZE + TILE_GAP) + TILE_GAP, y + TILE_GAP + (TILE_SIZE + TILE_GAP)*3))]]

        self.tiles = pygame.sprite.Group() #luo sprite group tileille

        '''tile_data on matriisi joka pitää kokoajan tiedon pelilaudan tilanteesta.
        Koska tiledata nykyään arvotaan toisessa funktiossa tein tähän esimerkin näyttämään miltä tiledata yleensä näyttää:
        self.tile_data = [[2,0,0,0],
                          [0,0,0,0],
                          [0,0,2,0],
                          [0,0,0,0]]
        esim näin
        '''
        self.tile_data = Grid.randomize_grid() #randomisoi ensimmäiset ruudut tiledataan
        self.set_tiles() #luo uudet Tile() oliot kohtiin jotka määräytyvät tiledatassa

        #asettaa scoren ja high scoren
        self.score = 0 
        self.high_score = Save_Manager.load()

        #luodaan vielä muutama hyödyllinen muuttuja animaatioita varten
        # self.animation_on = False
        # self.animation_timer = 0

        self.keys_pressed = [] #tallennetaan painetun näppäimen index, että pygame ymmärtää milloin näppäin painetaan alas

        #state muutujat
        self.game_over_state = False 


    def randomize_grid(): #randomisoi gridin alkutilanteen aina pelin alussa ja restartattaessa
        #arvo kaksi sijaintia 16 ruudun ruudukosta
        first_1 = random.randint(0,15) 
        first_2 = random.randint(0,15)

        if first_2 == first_1: first_2 += 1  #estetään että molemmat olisivat sama

        #tehdään tyhdä grid
        data =     [[0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]
        #käydään joka kohta läpi ja vaihdetaan oikeat indexit kakkosiksi
        i = 0
        for row in data:
            for col_i in range(len(row)):
                i += 1
                if i == first_1 or i == first_2:
                    row[col_i] = 2
        return data #palauta randomisoitu alkutilanne

    def get_score(self): #öö varmaan ihan turha
        #en tiedä yhtään miten pythonin ja pygamen turvaluokitus käytännöt toimii
        #tää on vaa unityssä suosittu tapa ettei suoraan katsota toisen olion dataa
        #mahdollistaa myös jos tässä sisällä pitäis viel muokata jotain yms
        #tällä hetkellä aivan turha
        return self.score
    
    def get_high_score(self): #sama kun ylempi
        #täysin sama kuin ylempi
        return self.high_score

    def set_tiles(self): #luo uudet tilet tile_data ruudukon mukaan
        '''
        en tiedä olenko ylpeä siitä, 
        että joka liikkeen jälkeen pitää uudelleen luoda tilet uudelleen
        mutta se toimii eikä tässä scaalassa tuota liikaa lagia.
        Tämä on yhdistymisien ja muutenkin alkutilanteen takia helpompaa kuin liikuttaminen,
        vaikka nykyään pelissä onkin koodi liikkumisanimaatioille
        '''
        self.tiles.empty() #tyhjennä vanhat tilet spritegroupista
        
        #käy koko tile_data läpi
        for row_i, row  in enumerate(self.tile_data):
            for col_i, cell in enumerate(row):

                if(cell != 0): #jos ruutu ei ole tyhjä

                    world_pos = self.tile_poses[row_i][col_i] #hae/tallenna muokattavan ruudun pikselisijainti
                    
                    #käytän 1 ja 3 tallentamaan uudet tilet
                    if (cell == 1): 
                        row[col_i] = 2 #vaihtaa 1-> 2
                        self.tiles.add(Tile((row_i, col_i),world_pos[0], world_pos[1], 2, True))
                    elif (cell == 3):
                        row[col_i] = 4 #vaihtaa 3-> 4
                        self.tiles.add(Tile((row_i, col_i),world_pos[0], world_pos[1], 4, True))
                    else: #Luo uuden tile olion annettuun kohtaan annetulla valuella
                        self.tiles.add(Tile((row_i, col_i),world_pos[0], world_pos[1], cell)) 
   
    """  def create_tile_animation(self, _row, _col, des_row, des_col, _dir): #laskee ja asetta yksittäisen tilen nopeuden
        pos = self.tile_poses[_row][_col] #lähtökohta
        des = self.tile_poses[des_row][des_col] #siirtymä kohde

        dir = [0,0]
        #laske suunta ja nopeus (nopeus riippuu matkan pituudesta, jotta kaikki ovat perillä yhtäaikaa)
        if des[0] != pos[0]:
            speed =  abs(des[0] - pos[0]) / TILE_ANIM_LENGTH
            dir[0] = speed * _dir
        elif des[1] != pos[1]:
            speed =  abs(des[1] - pos[1]) / TILE_ANIM_LENGTH
            dir[1] = speed * _dir
        
        #etsi tarvittu tile tilespriteistä
        tile = next((x for x in self.tiles.sprites() if x.grid_pos == (_row, _col)), None)
        if tile:
            tile.set_animation_dir(dir) #aseta tilelle laskettu suunta
        else:
            print('error?') #jos tileä ei löydy jota ei pitäisi koskaan tapahtua """
        
    def check_tile(self, _tile, _row, _col, _max, _min, max_dir, reverse = False)-> int: #tarkistaa yksittäisen ruudun liikutusmahdollisuudet
        #koodi on hieman sekava myönnän
        #suurin osa johtuu siitä koska tämä sama aliohjelma hallitsee sekä horizontaalisen, että verticaalisen liikkeen
        #sekä molemmat sekä ylös/alas, ja vasen/oikea 
        #joten pitää käyttää paljon epämääräisiä muuttujia ja parametreja

        if _tile != 0: #jos liikutettava eli tässä ruudussa on jotain
            self.tile_data[_row][_col] = 0 #poistetaan vanhasta siainnista
            target_tile = self.tile_data[_row if not reverse else _max][_max if not reverse else _col] #asetetaan kohde mahdollisimman pitkälle
            while target_tile != 0 and target_tile != _tile and _max != _min: #etsitään tyhjää kohtaa tai samaa numeroa jotta voidaan yhdistyä
                _max += max_dir #siirrytään seuraavaan pienentämällä/suurentamalla maksimia
                target_tile = self.tile_data[_row if not reverse else _max][_max if not reverse else _col] #uudelleen asetetaan kohde uusia testejä varten

            #jos palaa samaan kohtaan mistä lähti
            if ((_row == _max and reverse) or (_col == _max and not reverse)): 
                self.tile_data[_row][_col] = _tile #asetetaan arvo takaisin
                return _max, False #palautetaan maksimi käyttöä varten ja tieto ettei ruutua liikutettu

            if _tile == target_tile: #jos löytää saman arvon kun oma arvo
                self.tile_data[_row if not reverse else _max][_max if not reverse else _col] = _tile * 2 #asetetaan kaksinkertainen arvo
                self.score += _tile * 2 #lisää score yhdistymisestä

                _max += max_dir #lisää maxia ettei kaksi yhdisty samal kerral
            else: #muussa tapauksessa (= löysi tyhjän kohdan)
                self.tile_data[_row if not reverse else _max][_max if not reverse else _col] = _tile #lisää arvo tähän kohtaan

            return _max, True #palauta tieto että ruutua liikutettiin
        return _max, False #ruutua ei liikutettu
            
    def move_manager(self, dir: tuple): #hallitseee gridin siirron yhteen suuntaan
        moved = False #tieto onnistuiko liikuttaminen
        moved_vali = False #välitieto onnistumisen selvittämiseen

        if dir[0] != 0: #horizontal
            if dir[0] == 1: #liikutus oikealle
                #käy läpi joka rivi
                for row in range(0, 4, 1):
                    max = 3
                    #käy rivin kohdat oikealta vasemmalle
                    for col in range(2, -1, -1):
                        tile = self.tile_data[row][col] #ota kyseinen ruutu
                        max, moved_vali = self.check_tile(tile, row, col, max, 0, -1) #tarkista/liikuta ruutua jos pystyy
                        if moved_vali: #jos liikkui
                            moved = True #aseta tieto liikuttamisen onnistumisesta
            else:  #vasemmalle
                #muuten sama kuin edellinen paitsi rivin kohdat käydään oikealta vasemmalle
                for row in range(0, 4, 1):
                    min = 0
                    for col in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        min, moved_vali = self.check_tile(tile, row, col, min, 3, 1)
                        if moved_vali:
                            moved = True
        else: #vertical
            #sama kuin edelliset paitsi käydään ensin jonot ja sitten rivit asetetussa suunnassa
            if dir[1] == 1: #alas
                for col in range(0, 4, 1):
                    max = 3
                    for row in range(2, -1, -1):
                        tile = self.tile_data[row][col]
                        max, moved_vali = self.check_tile(tile, row, col, max, 0, -1, True)
                        if moved_vali:
                            moved = True
            else: #ylös
                for col in range(0, 4, 1):
                    min = 0
                    for row in range(1, 4, 1):
                        tile = self.tile_data[row][col]
                        min,moved_vali = self.check_tile(tile, row, col, min, 3, 1, True)
                        if moved_vali:
                            moved = True

        if moved: #jos jokin liikkui = liikuttaminen suuntaan onnistuu
            #aseta uusi ruutu            
            self.set_new_tile(True) #true parametrilla asettaa uuden tilen
        else: #jos mikään ei liikkunut
            self.set_new_tile(False) #false parametrilla metodi vain tarkistaa oletko hävinnyt pelin
        self.set_tiles()
    
    def set_new_tile(self, set): #aseta uusi ruutu
        new_pos = (random.randint(0, 3), random.randint(0, 3)) #arvo kohta
        vapaat_paikat = [(0,0),(0,1),(0,2),(0,3),
                (1,0),(1,1),(1,2),(1,3),
                (2,0),(2,1),(2,2),(2,3),
                (3,0),(3,1),(3,2),(3,3)]

        while self.tile_data[new_pos[0]][new_pos[1]] != 0 and vapaat_paikat: #kunnes arvottu kohta on vapaa
            vapaat_paikat.remove(new_pos) #poista kohta vapaista
            if not vapaat_paikat:#jos vapaat paikat loppuvat=ruudukko on täynnä
                break #pakene loopista

            new_pos = random.choice(vapaat_paikat) #arvo uusi kohta jäljelle jääneistä vapaista
        
        if vapaat_paikat and set: #jos halutaan asettaa ruutu ja sille löytyy paikka
            self.tile_data[new_pos[0]][new_pos[1]] = random.choice((1,1,1,1,1,1,1,1,1,3)) #aseta ruutu ja arvo sen arvoksi 1(=2) tai 3(4)
        elif not vapaat_paikat: #jos ei vapaita paikkoja
            movable = False #selitetään voiko mitään ruutua yhdistää(=peli on jatkokelpoinen)
            for row in range(len(self.tile_data)):
                    for col in  range(len(self.tile_data[0])):
                        if self.neighbors(self.tile_data[row][col], row, col): #kerätään tieto yhdistämisestä joka tileä kohden
                            movable = True
            if not movable: self.game_over() #jos mitään ei voi yhdistää ja täynnä(=häviö)

    def neighbors(self, _tile, row_number, column_number): #kerää tiedot ruutujen naapureista häviämis tietoja varten
        a = self.tile_data #kopioi tiledata a
        #iso osittain netisä kopioitu ja muokattu listaoperaattori
        #kerää jokaisen tilen viereisen tilen JOS ne ovat sama
        #en selitä kaikkia listaoperaattorin ehtoja, se vain katsoo että kaikki ehdot täyttyvät
        lista = [a[i][j]  
            for i in range(row_number-1, row_number+2) 
                for j in range(column_number-1, column_number+2) 
                    if i > -1 and j > -1 and j < len(a[0]) and i < len(a) and (((i == row_number) or (j == column_number)) and not(j == column_number and i == row_number)) and a[i][j] == _tile]
        return lista #palauta lista, (jos tyhjä ei ole yhtään viereisä samoja)(jos ei tyhjä on viereisiä samoja)

    def get_input(self): #lukee tietokone inputteja ja kutsuu muita metodeja
        keys = pygame.key.get_pressed() #kerää input tiedot dictionaryyn

        '''tarkistaa jokaista haluttua näppäintä kohden:
        -painetaanko kyseistä näppäintä
        -mikään muu (haluttu) nappi ei ole painettuna alas
        sitten:
        -lisää tieto että nappi on painettu
        -kutsu tieto liikuttamiseen haluttuun suuntaan
        supporttaa wasd sekä nuolinäppäin controllit
        '''
        if keys[pygame.K_RIGHT] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_RIGHT)
            self.move_manager((1,0))
        elif keys[pygame.K_LEFT] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_LEFT)
            self.move_manager((-1,0))
        elif keys[pygame.K_DOWN] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_DOWN)
            self.move_manager((0,1))
        elif keys[pygame.K_UP] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_UP)
            self.move_manager((0,-1))
        elif keys[pygame.K_d] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_d)
            self.move_manager((1,0))
        elif keys[pygame.K_a] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_a)
            self.move_manager((-1,0))
        elif keys[pygame.K_s] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_s)
            self.move_manager((0,1))
        elif keys[pygame.K_w] and not self.keys_pressed:
            self.keys_pressed.append(pygame.K_w)
            self.move_manager((0,-1))
        elif self.keys_pressed and not keys[self.keys_pressed[0]]: #hallitsee napista irtipäästön
            self.keys_pressed.pop(0) #poistaa napin painetuista

    def game_over(self): #asettaa pelin häviötilaan
        if self.score > self.high_score: #jos score on uusi highscore
            #vaihda ja tallenna highscore
            self.high_score = self.score 
            Save_Manager.save(self.high_score)
        self.image.fill(pygame.color.Color('red'))
        self.game_over_state = True #aseta tila häviötilaan

    """ def animate_tiles(self): #liikuttaa jokaista tileä oman nopeutensa verran
        for tile in self.tiles.sprites():
            tile.animate() #liikuta jokaista tileä

        self.animation_on = False if self.animation_timer >= TILE_ANIM_LENGTH else True #jos animaatio on valmis, poistu animaatiotilasta
        self.animation_timer += 1 #kasvata animaatiotimeria
        if not self.animation_on: #jos animaatio on valmis
            self.set_tiles() #uudelleenluo tilet (= joka on tyhmää mutta paras ratkaisu) """
    
    def reset(self): #uudelleen aloittaa pelin häviön jälkeen
        self.game_over_state = False #poistaa häviötilan
        self.image.fill((255, 255, 240))
        self.tile_data = Grid.randomize_grid() #uudelleen arpoo ruudukon
        self.score = 0 #nollaa pisteet
        self.set_tiles() #uudelleen luo tilet

    def continue_game(self): #jatkaa peliä voiton jälkeen
        self.game_won_state = False #poistaa voitto staten
        self.set_tiles() #varmuudksi uudellenasettaa tilet(ehkä turhaa)


    def update(self, display): #päivitystä kutsutaan mainista joka frame
        
        self.tiles.draw(display) #piirtää listan tilet ikkunaan
        self.tiles.update(display)  #päivittää tilejen tiedot

        if not (self.game_over_state):
            self.get_input() #hae inputteja
        