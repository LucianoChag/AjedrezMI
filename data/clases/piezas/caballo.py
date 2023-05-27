import pygame
from data.clases.Pieza import Pieza

class Caballo(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_caballo.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 30, tablero.tile_alto - 30))
        self.notacion = 'C'

    def get_posibles_movimientos(self, tablero):
        output = []
        movimientos = [
            (1, -2),
            (2, -1),
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2)
        ]
        for movimiento in movimientos:
            nueva_pos = (self.x + movimiento[0], self.y + movimiento[1])
            if (
                nueva_pos[0] < 8 and
                nueva_pos[0] >= 0 and 
                nueva_pos[1] < 8 and 
                nueva_pos[1] >= 0
            ):
                output.append([
                    tablero.get_cuadricula_desde_pos(
                        nueva_pos
                    )
                ])
        return output