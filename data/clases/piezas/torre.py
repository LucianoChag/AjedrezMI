import pygame

from data.clases.Pieza import Pieza

class Torre(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_torre.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 30, tablero.tile_alto - 30))
        self.notacion = 'T'

    def get_posibles_movimientos(self, tablero):
        output = []
        mover_norte = []
        for y in range(self.y)[::-1]:
            mover_norte.append(tablero.get_cuadricula_desde_pos(
                (self.x, y)
            ))
        output.append(mover_norte)
        mover_este = []
        for x in range(self.x + 1, 8):
            mover_este.append(tablero.get_cuadricula_desde_pos(
                (x, self.y)
            ))
        output.append(mover_este)
        mover_sur = []
        for y in range(self.y + 1, 8):
            mover_sur.append(tablero.get_cuadricula_desde_pos(
                (self.x, y)
            ))
        output.append(mover_sur)
        mover_oeste = []
        for x in range(self.x)[::-1]:
            mover_oeste.append(tablero.get_cuadricula_desde_pos(
                (x, self.y)
            ))
        output.append(mover_oeste)
        return output