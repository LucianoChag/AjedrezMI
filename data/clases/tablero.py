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