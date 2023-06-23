import json
import sys
import os
import pygame
from data.clases.cuadricula import Cuadricula
from data.clases.button import Button
from data.clases.tablero import Tablero

pygame.init()

FONDO = pygame.image.load("data/imgs/fondo.png")
WINDOW_SIZE = (750, 650)
screen = pygame.display.set_mode(WINDOW_SIZE)

tablero = Tablero(WINDOW_SIZE[0], WINDOW_SIZE[1])
cuadricula = Cuadricula

def draw(display):
	display.fill('white')
	tablero.dibujar(display)
	pygame.display.update()


def get_font(size): 
    return pygame.font.Font("data/imgs/font.ttf", size)

  
    
def menu_principal():
    pygame.display.set_caption("Menú Principal")
    while True:
        screen.blit(FONDO,(0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(52).render("MENU PRINCIPAL", True, "#080807")
        MENU_RECT = MENU_TEXT.get_rect(center=(380,120))
        
        NUEVA_PARTIDA_BUTTON = Button(image=pygame.image.load("data/imgs/Nueva Partida.png"), pos=(380, 250), text_input="NUEVA PARTIDA", font=get_font(42), base_color="#d7fcd4", hovering_color="White")
        
        CONTINUAR_BUTTON = Button(image=pygame.image.load("data/imgs/Continuar.png"), pos=(380, 400), text_input="CONTINUAR", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        
        SALIR_BUTTON = Button(image=pygame.image.load("data/imgs/Salir.png"), pos=(380, 550), text_input="SALIR", font=get_font(42), base_color="#d7fcd4", hovering_color="White")
        
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [NUEVA_PARTIDA_BUTTON, CONTINUAR_BUTTON, SALIR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NUEVA_PARTIDA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    nueva_partida()
                if CONTINUAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    continuar()
                if SALIR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def nueva_partida():
    pygame.display.set_caption("Ajedrez")
    game_running = True
    tablero.reiniciar_tablero()
    while game_running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse is clicked
                if event.button == 1:
                    tablero.handle_click(mx, my)
        if tablero.esta_en_jaque_mate('black'):  # If black is in checkmate
            print('White wins!')
            game_running = False
        elif tablero.esta_en_jaque_mate('white'):  # If white is in checkmate
            print('Black wins!')
            game_running = False
        if tablero.turno == 'black':
            # Obtener el mejor movimiento del bot
            tablero.realizar_movimiento_bot()
        # Draw the board
        draw(screen)

def continuar():
    pygame.display.set_caption("Ajedrez")
    game_running = True
    tablero.cargar_estado()

    while game_running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse is clicked
                if event.button == 1:
                    tablero.handle_click(mx, my)
        if tablero.esta_en_jaque_mate('black'):  # If black is in checkmate
            print('White wins!')
            game_running = False
        elif tablero.esta_en_jaque_mate('white'):  # If white is in checkmate
            print('Black wins!')
            game_running = False
        if tablero.turno == 'black':
            tablero.realizar_movimiento_bot()
        # Draw the board
        draw(screen)


menu_principal()