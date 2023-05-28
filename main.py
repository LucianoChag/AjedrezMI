import pygame

from data.clases.tablero import Tablero

pygame.init()

WINDOW_SIZE = (650, 650)
screen = pygame.display.set_mode(WINDOW_SIZE)

tablero = Tablero(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
	display.fill('white')
	tablero.dibujar(display)
	pygame.display.update()


if __name__ == '__main__':
	game_running = True
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
		if tablero.esta_en_jaque_mate('black'): # If black is in checkmate
			print('White wins!')
			game_running = False
		elif tablero.esta_en_jaque_mate('white'): # If white is in checkmate
			print('Black wins!')
			game_running = False
		# Draw the board
		draw(screen)