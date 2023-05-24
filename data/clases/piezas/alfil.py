import pygame
from data.clases.Pieza import Pieza

class Alfil(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_alfil.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 20, tablero.tile_alto - 20))
        self.notation = 'A'

    def get_movimientos_validos(self, tablero):
        salida = []

        mueve_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            mueve_ne.append(tablero.get_cuadricula_desde_pos(
                (self.x + i, self.y - i)
            ))
        salida.append(mueve_ne)

        mueve_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            mueve_se.append(tablero.get_cuadricula_desde_pos(
                (self.x + i, self.y + i)
            ))
        salida.append(mueve_se)

        mueve_so = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            mueve_so.append(tablero.get_cuadricula_desde_pos(
                (self.x - i, self.y + i)
            ))
        salida.append(mueve_so)

        mueve_no = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            mueve_no.append(tablero.get_cuadricula_desde_pos(
                (self.x - i, self.y - i)
            ))
        salida.append(mueve_no)
        
        return salida
