import pygame, sys
import ctypes

from data.defs import *
from data.grid import Grid

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

    #luodaan grid eli ruudukko joka halinnoi kaiken gameplay logiikan
    grid = Grid()
    grid_sprite = pygame.sprite.GroupSingle(grid)

    #luodaan teksti fontteja joiden käyttö on tosi epäloogista ja ympäri koodia mutten nyt ala siistimäänkään
    text_font = pygame.font.SysFont("arial Black", FONT_SIZE_2)
    go_text_font = pygame.font.SysFont("calibri Black", FONT_SIZE_1)
    #haetaan kuvat häviö ja voitto stateen kansiosta (ainoa artti pelissä)
    game_over_bc = pygame.image.load(BC_BLACK_ART)
    game_won_bc = pygame.image.load(BC_YELLOW_ART)

    #pistetään peli käyntiin
    running = True

    while running:
        #pistää max framerateksi 60, toivottavasti ei mene myöskään sitä alemmaksi
        #toisinsanoen tämä while loop mikä hallitsee muita pelin asioita, tapahtuu vain 60 kertaa sekunnissa, eikä sitä normaalia 100-1000 mitä se ehkä voisi pyörittää
        clock.tick(FPS) 

        #pygame eventtejen hallinta
        for event in pygame.event.get():
            #sammuttaa pelin sulkiessa
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            
            #game_over ja game_won statesta poispääsy inputtien avulla, helpompi tehdä täällä kuin gridissä
            if grid.game_over_state and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid.reset()
            if grid.game_won_state and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.continue_game()
        
        #värjää taustan 
        SCREEN.fill("#FFDFAA")
        #piirtää ja kutsuu ruudukon päivitystoimintoa
        grid_sprite.draw(SCREEN)
        grid_sprite.update(SCREEN)

        #piirtää scoren ja highscoren
        display_text(str(grid.get_score()), text_font, (TEXT_OFFSET, 100), (0,0,0))
        display_text(str(grid.get_high_score()), text_font, (WIDTH - TEXT_OFFSET, 100), (0,0,0))
        #piirtää otsikot niille
        display_text('SCORE:', go_text_font, (TEXT_OFFSET, 50), (0,0,0))
        display_text('HIGHSCORE:', go_text_font, (WIDTH - TEXT_OFFSET, 50), (0,0,0))

        if grid.game_over_state: #jos peli hävitty
            SCREEN.blit(game_over_bc, (0,0)) #gameover kuva
            display_text('''GAME OVER \n PRESS "R" TO RETRY''', go_text_font, (WIDTH / 2, HEIGHT / 2), (255, 50,50)) #piirrä gameover teksti
        if grid.game_won_state: #jos peli voitettu
            SCREEN.blit(game_won_bc, (0,0)) #gamewon kuva
            display_text('''YOU WON \n PRESS "SPACE" TO CONTINUE''', go_text_font, (WIDTH / 2, HEIGHT / 2), (50, 255,150)) #piirrä gamewon teksti

        pygame.display.update() #päivitetään ikkuna johon muutokset on tehty

if __name__ ==  "__main__": #tarkistetaan namespace koska kaikki aina netissä käskee :D
    run_game()
