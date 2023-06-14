import pygame

from data.clases.pieza import Pieza

class Peon(Pieza):
    def __init__(self, pos, color, tablero):
        super().__init__(pos, color, tablero)
        img_path = 'data/imgs/' + color[0] + '_peon.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tablero.tile_ancho - 45, tablero.tile_alto - 45))
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
            nueva_pos = (self.x, self.y + movimiento[1])
            if nueva_pos[1] < 8 and nueva_pos[1] >= 0:
                output.append(
                    tablero.get_cuadricula_desde_pos(nueva_pos)
                )
        return output

    def get_movimientos(self, tablero):
        output = []
        for cuadricula in self.get_posibles_movimientos(tablero):
            if cuadricula.ocupando_espacio!= None:
                break 
            else:
                output.append(cuadricula)
        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x + 1, self.y - 1)
                )
                if cuadricula.ocupando_espacio != None:
                    if cuadricula.ocupando_espacio.color != self.color:
                        output.append(cuadricula)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x - 1, self.y - 1)
                )
                if cuadricula.ocupando_espacio != None:
                    if cuadricula.ocupando_espacio.color != self.color:
                        output.append(cuadricula)
        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x + 1, self.y + 1)
                )
                if cuadricula.ocupando_espacio != None:
                    if cuadricula.ocupando_espacio.color != self.color:
                        output.append(cuadricula)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                cuadricula = tablero.get_cuadricula_desde_pos(
                    (self.x - 1, self.y + 1)
                )
                if cuadricula.ocupando_espacio!= None:
                    if cuadricula.ocupando_espacio.color != self.color:
                        output.append(cuadricula)
        return output

    def atacando_cuadriculas(self, tablero):
        movimientos = self.get_movimientos(tablero)
        # retornar movimientos diagonales
        return [i for i in movimientos if i.x != self.x]


    def obtener_informacion(self):
        return {
            "posicion": self.pos,
            "color": self.color
        }