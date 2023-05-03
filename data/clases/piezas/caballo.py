import pygame
from data.clases.pieza import Pieza

class Caballo(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_knight.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 20, tablero.tile_alto - 20))
        self.notacion = 'C'