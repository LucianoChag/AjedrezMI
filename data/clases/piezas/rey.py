import pygame
from data.clases.pieza import Pieza

class Rey(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_rey.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 20, tablero.tile_alto - 20))
        self.notation = 'R'

    def get_posibles_movimientos(self, tablero):
        output = []
        movimientos = [
            (0,-1), # norte
            (1, -1), # ne
            (1, 0), # este
            (1, 1), # se
            (0, 1), # sur
            (-1, 1), # so
            (-1, 0), # oeste
            (-1, -1), # no
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

    def can_castle(self, tablero):
        if not self.se_ha_movido:
            if self.color == 'white':
                queenside_rook = tablero.get_pieza_desde_pos((0, 7))
                kingside_rook = tablero.get_pieza_desde_pos((7, 7))
                if queenside_rook != None:
                    if not queenside_rook.se_ha_movido:
                        if [
                            tablero.get_pieza_desde_pos((i, 7)) for i in range(1, 4)
                        ] == [None, None, None]:
                            return 'queenside'
                if kingside_rook != None:
                    if not kingside_rook.se_ha_movido:
                        if [
                            tablero.get_pieza_desde_pos((i, 7)) for i in range(5, 7)
                        ] == [None, None]:
                            return 'kingside'
            elif self.color == 'black':
                queenside_rook = tablero.get_pieza_desde_pos((0, 0))
                kingside_rook = tablero.get_pieza_desde_pos((7, 0))
                if queenside_rook != None:
                    if not queenside_rook.se_ha_movido:
                        if [
                            tablero.get_pieza_desde_pos((i, 0)) for i in range(1, 4)
                        ] == [None, None, None]:
                            return 'queenside'
                if kingside_rook != None:
                    if not kingside_rook.se_ha_movido:
                        if [
                            tablero.get_pieza_desde_pos((i, 0)) for i in range(5, 7)
                        ] == [None, None]:
                            return 'kingside'

    def get_movimientos_validos(self, tablero):
        output = []
        for cuadricula in self.get_movimientos(tablero):
            if not tablero.esta_es_jaque(self.color, board_change=[self.pos, cuadricula.pos]):
                output.append(cuadricula)
        if self.can_castle(tablero) == 'queenside':
            output.append(
                tablero.get_cuadricula_desde_pos((self.x - 2, self.y))
            )
        if self.can_castle(tablero) == 'kingside':
            output.append(
                tablero.get_cuadricula_desde_pos((self.x + 2, self.y))
            )
        return output