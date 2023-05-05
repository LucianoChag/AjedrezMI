import pygame
from data.clases.cuadricula import Cuadricula
from data.clases.piezas.torre import Torre
from data.clases.piezas.alfil import Alfil
from data.clases.piezas.peon import Peon
from data.clases.piezas.rey import Rey
from data.clases.piezas.reina import Reina
from data.clases.piezas.caballo import Caballo

# comprobando el estado del juego
class Tablero:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.tile_ancho = ancho // 8
        self.tile_alto = alto // 8
        self.pieza_seleccionada = None
        self.turno = 'white'
        self.config = [
            ['nT', 'nC', 'nA', 'nQ', 'nR', 'nA', 'nC', 'nT'],
            ['nP', 'nP', 'nP', 'nP', 'nP', 'nP', 'nP', 'nP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['bT', 'bC', 'bA', 'bQ', 'bR', 'bA', 'bC', 'bT'],
        ]
        self.cuadriculas = self.generar_cuadriculas()
        self.setup_tablero()

#Generamos las cuadriculas en el tablero
    def generar_cuadriculas(self):
        salida = []
        for y in range(8):
            for x in range(8):
                salida.append(
                    Cuadricula(x,  y, self.tile_ancho, self.tile_alto)
                )
        return salida

    def get_cuadricula_desde_pos(self, pos):
        for cuadricula in self.cuadriculas:
            if (cuadricula.x, cuadricula.y) == (pos[0], pos[1]):
                return cuadricula

    def get_pieza_desde_pos(self, pos):
        return self.get_cuadricula_desde_pos(pos).ocupando_espacio

#Seteamos el tablero con su correspondiente pieza
    def setup_tablero(self):
        for y, fila in enumerate(self.config):
            for x, pieza in enumerate(fila):
                if pieza != '':
                    cuadricula = self.get_cuadricula_desde_pos((x, y))
                    #Miramos dentro del contenido a ver que pieza corresponde
                    if pieza[1] == 'T':
                        cuadricula.ocupando_espacio = Torre(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )
                    elif pieza[1] == 'C':
                        cuadricula.ocupando_espacio = Caballo(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )
                    elif pieza[1] == 'A':
                        cuadricula.ocupando_espacio = Alfil(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )
                    elif pieza[1] == 'Q':
                        cuadricula.ocupando_espacio = Reina(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )
                    elif pieza[1] == 'K':
                        cuadricula.ocupando_espacio = Rey(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )
                    elif pieza[1] == 'P':
                        cuadricula.ocupando_espacio = Peon(
                            (x, y), 'white' if pieza[0] == 'b' else 'black', self
                        )

#Funcion para determinar si hicieron click en alguna cuadricula
    def handle_click(self, mx, my):
        x = mx // self.tile_ancho
        y = my // self.tile_alto
        cuadricula_clickeada = self.get_cuadricula_desde_pos((x, y))
        if self.pieza_seleccionada is None:
            if cuadricula_clickeada.ocupando_espacio is not None:
                if cuadricula_clickeada.ocupando_espacio.color == self.turno:
                    self.pieza_seleccionada = cuadricula_clickeada.ocupando_espacio
        elif self.pieza_seleccionada.mover(self, cuadricula_clickeada):
            self.turno = 'white' if self.turno == 'black' else 'black'
        elif cuadricula_clickeada.ocupando_espacio is not None:
            if cuadricula_clickeada.ocupando_espacio.color == self.turno:
                self.pieza_seleccionada = cuadricula_clickeada.ocupando_espacio

