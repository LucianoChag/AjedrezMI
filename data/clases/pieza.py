import pygame


class Pieza:
    def __init__(self, pos, color, tablero):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.se_ha_movido = False


    def mover(self, tablero, cuadricula, forzar=False):
        for i in tablero.cuadriculas:
            i.resaltado = False
        if cuadricula in self.get_movimientos_validos(tablero) or forzar:
            prev_cuadricula = tablero.get_cuadricula_desde_pos(self.pos)
            self.pos, self.x, self.y = cuadricula.pos, cuadricula.x, cuadricula.y
            prev_cuadricula.ocupando_espacio = None
            cuadricula.ocupando_espacio = self
            tablero.pieza_seleccionada = None
            self.se_ha_movido = True

            # promocion del peon
            if self.notacion == ' ':
                if self.y == 0 or self.y == 7:
                    from data.clases.piezas.reina import Reina
                    cuadricula.ocupando_espacio = Reina(
                        (self.x, self.y),
                        self.color,
                        tablero
                    )
            # Enroque
            if self.notacion == 'R':
                if prev_cuadricula.x - self.x == 2:
                    torre = tablero.get_pieza_desde_pos((0, self.y))
                    torre.mover(tablero, tablero.get_cuadricula_desde_pos((3, self.y)), forzar=True)
                elif prev_cuadricula.x - self.x == -2:
                    torre = tablero.get_pieza_desde_pos((7, self.y))
                    torre.mover(tablero, tablero.get_cuadricula_desde_pos((5, self.y)), forzar=True)
            return True
        else:
            tablero.pieza_seleccionada = None
            return False

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
    


    # Verdadero para todas las piezas excepto peon
    def atacando_cuadriculas(self, tablero):
        return self.get_movimientos(tablero)