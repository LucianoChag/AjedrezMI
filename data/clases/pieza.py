import pygame

class Pieza:
    def __init__(self, pos, color, tablero):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.se_ha_movido = False

    def get_movimientos(self, tablero):
        output = []
        for direction in self.get_posibles_movimientos(tablero):
            for cuadricula in direction:
                if cuadricula.ocupando_espacio is not None:
                    if cuadricula.ocupando_espacio.color == self.color:
                        break
                    else:
                        output.append(cuadricula)
                        break
                else:
                    output.append(cuadricula)
        return output
    
    def get_movimientos_validos(self, tablero):
        output = []
        for cuadricula in self.get_movimientos(tablero):
            if not tablero.esta_en_jaque(self.color, cambio_del_tablero=[self.pos, cuadricula.pos]):
                output.append(cuadricula)
        return output