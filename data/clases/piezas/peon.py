import pygame

from data.clases.pieza import Pieza

class Peon(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 35, tablero.tile_alto - 35))
        self.notacion = ' '