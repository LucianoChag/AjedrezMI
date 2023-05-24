import pygame

from data.clases.Pieza import Pieza

class Peon(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_peon.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 35, tablero.tile_alto - 35))
        self.notacion = ' '

    def get_posibles_movimientos(self, tablero):
        output = []
        movimientos = []
        # mover adelante
        if self.color == 'white':
            movimientos.append((0, -1))
            if not self.se_ha_movido:
                movimientos.append((0, -2))
        elif self.color == 'black':
            movimientos.append((0, 1))
            if not self.se_ha_movido:
                movimientos.append((0, 2))
        for movimiento in movimientos:
            new_pos = (self.x, self.y + movimiento[1])
            if new_pos[1] < 8 and new_pos[1] >= 0:
                output.append(
                    tablero.get_cuadricula_desde_pos(new_pos)
                )
        return output

    def get_movimientos(self, tablero):
        output = []
        for cuadricula in self.get_posibles_movimientos(tablero):
            if cuadricula.pieza_ocupada!= None:
                break 
            else:
                output.append(cuadricula)
        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x + 1, self.y - 1)
                )
                if cuadricula.ocupando_espacio != None:
                    if cuadricula.pieza_ocupada.color != self.color:
                        output.append(cuadricula)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x - 1, self.y - 1)
                )
                if cuadricula.pieza_ocupada != None:
                    if cuadricula.pieza_ocupada.color != self.color:
                        output.append(cuadricula)
        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x + 1, self.y + 1)
                )
                if cuadricula.pieza_ocupada != None:
                    if cuadricula.pieza_ocupada.color != self.color:
                        output.append(cuadricula)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x - 1, self.y + 1)
                )
                if cuadricula.pieza_ocupada!= None:
                    if cuadricula.pieza_ocupada.color != self.color:
                        output.append(cuadricula)
        return output

    def atacando_cuadriculas(self, tablero):
        movimientos = self.get_movimientos(tablero)
        # retornar movimientos diagonales
        return [i for i in movimientos if i.x != self.x]