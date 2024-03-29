import pygame, sys
import ctypes

from defs import *
from grid import Grid
from input_manager import Input_Manager

#pääosin pelin asetusten ja UI:n hallinnointia, sisältää peli logiikan häviö ja voitto screenille(koska UI) muttei paljon muuta
def run_game(): 
    
    #päätin että heitän metodit tähän ylimmäksi, näyttää erikoisen tyhmältä kuin tässä on vain yksi mutta näillä mennään

    def display_text(text: str, font: pygame.font.Font, pos, color): #tekstien piirtämistä helpoittava metodi
        lines = text.splitlines() #jakaa multiline tekstin riveihin
        for i, l in enumerate(lines):
            text_surf = font.render(l, True, color) #renderoi tekstit
            text_rect = text_surf.get_rect(center = pos) #luo niille rectanglet joila keskitys helpompaa
            SCREEN.blit(text_surf, (text_rect.x, text_rect.y +FONT_SIZE_1*i)) #hallitsee rivinvaihdon koon

    pygame.init() #käynnistää pygamen
    ctypes.windll.user32.SetProcessDPIAware() #fixaa resoluution windows laitteilla

    #perus pygame setuppaus juttuja
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 by Samuli")

    clock = pygame.time.Clock()

    #luodaan gridit eli ruudukot joka halinnoi kaiken gameplay logiikan
    #ruudukkojen sijainnit muistiin HUOM 1d lista!!!
    grid_poses = [(GRID_CAP, GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + (GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + 2*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + 3*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP),
                 (GRID_CAP, GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + (GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + 2*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + 3*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE)]

    grid_sprites = pygame.sprite.Group() #lista grideille
    grids_lost = pygame.sprite.Group() #lista kuolleille grideille
    grid_scores = {'A': [], 'B': [], 'A+B': [], 'B+A': [], 'M1': [], 'M2': [], 'R1': [], 'R2': []}
    index_names = ['A','B','A+B','B+A','M1', 'M2', 'R1', 'R2']

    for pos in grid_poses:
        grid_sprites.add(Grid(pos[0], pos[1]))



    #luodaan teksti fontteja joiden käyttö on tosi epäloogista ja ympäri koodia mutten nyt ala siistimäänkään
    text_font = pygame.font.SysFont("arial", FONT_SIZE_2)
    go_text_font = pygame.font.SysFont("calibri Black", FONT_SIZE_1)
    #haetaan kuvat häviö ja voitto stateen kansiosta (ainoa artti pelissä)
    game_over_bc = pygame.image.load(BC_RED_ART)

    #ai stufd begins
    gen = 0 #generaatio mis mennään

    highest_score = 0

    #pistetään peli käyntiin
    running = True

    while running:
        #pistää max framerateksi 60, toivottavasti ei mene myöskään sitä alemmaksi
        #toisinsanoen tämä while loop mikä hallitsee muita pelin asioita, tapahtuu vain 60 kertaa sekunnissa, eikä sitä normaalia 100-1000 mitä se ehkä voisi pyörittää
        delta_time = clock.tick(FPS) 
        fps = 1000 / delta_time

        #pygame eventtejen hallinta
        for event in pygame.event.get():
            #sammuttaa pelin sulkiessa
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            
            #game_over ja game_won statesta poispääsy inputtien avulla, helpompi tehdä täällä kuin gridissä
            # if grid.game_over_state and event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:
            #         grid.reset()
        
        #värjää taustan 
        SCREEN.fill("#FFDFAA")
        #piirtää ja kutsuu ruudukon päivitystoimintoa
        grid_sprites.draw(SCREEN)
        grid_sprites.update(SCREEN)

        #piirtää scoren ja highscoren

        for grid in grid_sprites.sprites(): #piirretään jokaiselle score
            grid: Grid
            display_text(str(grid.get_score()), text_font, (grid.rect.x +10, grid.rect.y+10), (0,0,0))
            if grid.game_over_state and not grid in grids_lost: #jos kuollut
                grids_lost.add(grid) #lisää kuolleisiin
                grid_sprites.remove(grid) #poistetaan elosa säästääkseen fps

        grids_lost.draw(SCREEN)

        if len(grids_lost) == 8: #jos kaikki on kuolut
            for i, grid in enumerate(grids_lost.sprites()): 
                if grid.score > highest_score: highest_score = grid.score
                grid_scores[index_names[i]].append(grid.score)
                grid.reset() #reset kaikki
            gen += 1
            grid_sprites = pygame.sprite.Group(grids_lost.sprites()) #lisätään takaisin listaan
            grids_lost.empty()

        Input_Manager.randomize_for_grids(grid_sprites.sprites())


        #piirtää otsikot niille
        display_text('FPS: ' + str(round(fps/100,1)*100), go_text_font, (WIDTH //2, 25), (0,0,0))
        display_text('GEN:' + str(gen), go_text_font, (TEXT_OFFSET, 50), (0,0,0))
        display_text(str(highest_score) +'HIGHSCORE', go_text_font, (WIDTH - TEXT_OFFSET, 50), (0,0,0))



        pygame.display.update() #päivitetään ikkuna johon muutokset on tehty

if __name__ ==  "__main__": #tarkistetaan namespace koska kaikki aina netissä käskee :D
    run_game()
