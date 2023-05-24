import pygame
from data.clases.pieza import Pieza

class Reina(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_reina.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 20, tablero.tile_alto - 20))
        self.notation = 'Q'

def get_posibles_movimientos(self, tablero):
        output = []
        mover_norte = []
        for y in range(self.y)[::-1]:
            mover_norte.append(tablero.get_cuadricula_desde_pos(
                (self.x, y)
            ))
        output.append(mover_norte)
        mover_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            mover_ne.append(tablero.get_cuadricula_desde_pos(
                (self.x + i, self.y - i)
            ))
        output.append(mover_ne)
        mover_este = []
        for x in range(self.x + 1, 8):
            mover_este.append(tablero.get_cuadricula_desde_pos(
                (x, self.y)
            ))
        output.append(mover_este)
        mover_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            mover_se.append(tablero.get_cuadricula_desde_pos(
                (self.x + i, self.y + i)
            ))
        output.append(mover_se)
        mover_sur = []
        for y in range(self.y + 1, 8):
            mover_sur.append(tablero.get_cuadricula_desde_pos(
                (self.x, y)
            ))
        output.append(mover_sur)
        mover_so = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            mover_so.append(tablero.get_cuadricula_desde_pos(
                (self.x - i, self.y + i)
            ))
        output.append(mover_so)
        mover_oeste = []
        for x in range(self.x)[::-1]:
            mover_oeste.append(tablero.get_cuadricula_desde_pos(
                (x, self.y)
            ))
        output.append(mover_oeste)
        mover_no = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            mover_no.append(tablero.get_cuadricula_desde_pos(
                (self.x - i, self.y - i)
            ))
        output.append(mover_no)
        return output