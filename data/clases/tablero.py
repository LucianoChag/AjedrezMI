import json
import os
import pygame
import random
from data.clases.cuadricula import Cuadricula
from data.clases.piezas.torre import Torre
from data.clases.piezas.alfil import Alfil
from data.clases.piezas.peon import Peon
from data.clases.piezas.rey import Rey
from data.clases.piezas.reina import Reina
from data.clases.piezas.caballo import Caballo

ARCHIVO_GUARDADO = "autoguardado.json"


# comprobando el estado del juego
class Tablero:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.tile_ancho = ancho // 8
        self.tile_alto = alto // 8
        self.pieza_seleccionada = None
        self.turno = "white"
        self.config = [
            ["bT", "bC", "bA", "bQ", "bR", "bA", "bC", "bT"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wT", "wC", "wA", "wQ", "wR", "wA", "wC", "wT"],
        ]
        self.cuadriculas = self.generar_cuadriculas()
        self.setup_tablero()

    # Generamos las cuadriculas en el tablero
    def generar_cuadriculas(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(Cuadricula(x, y, self.tile_ancho, self.tile_alto))
        return output

    def get_cuadricula_desde_pos(self, pos):
        for cuadricula in self.cuadriculas:
            if (cuadricula.x, cuadricula.y) == (pos[0], pos[1]):
                return cuadricula

    def get_pieza_desde_pos(self, pos):
        return self.get_cuadricula_desde_pos(pos).ocupando_espacio

    # Seteamos el tablero con su correspondiente pieza
    def setup_tablero(self):
        cuadriculas = []
        for y, fila in enumerate(self.config):
            for x, pieza in enumerate(fila):
                if pieza != "":
                    cuadricula = self.get_cuadricula_desde_pos((x, y))
                    # Miramos dentro del contenido a ver que pieza corresponde
                    if pieza[1] == "T":
                        cuadricula.ocupando_espacio = Torre(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    elif pieza[1] == "C":
                        cuadricula.ocupando_espacio = Caballo(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    elif pieza[1] == "A":
                        cuadricula.ocupando_espacio = Alfil(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    elif pieza[1] == "Q":
                        cuadricula.ocupando_espacio = Reina(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    elif pieza[1] == "R":
                        cuadricula.ocupando_espacio = Rey(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    elif pieza[1] == "P":
                        cuadricula.ocupando_espacio = Peon(
                            (x, y), "white" if pieza[0] == "w" else "black", self
                        )
                    cuadriculas.append(cuadricula)
        return cuadriculas

    # Funcion para determinar si hicieron click en alguna cuadricula
    def handle_click(self, mx, my):
        x = mx // self.tile_ancho
        y = my // self.tile_alto
        cuadricula_clickeada = self.get_cuadricula_desde_pos((x, y))
        if self.pieza_seleccionada is None:
            if cuadricula_clickeada.ocupando_espacio is not None:
                if cuadricula_clickeada.ocupando_espacio.color == self.turno:
                    self.pieza_seleccionada = cuadricula_clickeada.ocupando_espacio
        elif self.pieza_seleccionada.mover(self, cuadricula_clickeada):
            self.turno = "white" if self.turno == "black" else "black"
            self.guardar_estado()
        elif cuadricula_clickeada.ocupando_espacio is not None:
            if cuadricula_clickeada.ocupando_espacio.color == self.turno:
                self.pieza_seleccionada = cuadricula_clickeada.ocupando_espacio

    # Checkeamos si el jugador está en jaque
    def esta_en_jaque(self, color, cambio_del_tablero=None):
        output = False
        rey_pos = None
        pieza_cambiante = None
        vieja_cuadricula = None
        nueva_cuadricula = None
        nueva_cuadricula_vieja_pieza = None
        if cambio_del_tablero is not None:
            for cuadricula in self.cuadriculas:
                if cuadricula.pos == cambio_del_tablero[0]:
                    pieza_cambiante = cuadricula.ocupando_espacio
                    vieja_cuadricula = cuadricula
                    if vieja_cuadricula is not None:
                        vieja_cuadricula.ocupando_espacio = None
            for cuadricula in self.cuadriculas:
                if cuadricula.pos == cambio_del_tablero[1]:
                    nueva_cuadricula = cuadricula
                    nueva_cuadricula_vieja_pieza = nueva_cuadricula.ocupando_espacio
                    if nueva_cuadricula is not None:
                        nueva_cuadricula.ocupando_espacio = pieza_cambiante
        piezas = [
            i.ocupando_espacio
            for i in self.cuadriculas
            if i.ocupando_espacio is not None
        ]
        if pieza_cambiante is not None:
            if pieza_cambiante.notacion == "R":
                rey_pos = nueva_cuadricula.pos
        if rey_pos is None:
            for pieza in piezas:
                if pieza.notacion == "R" and pieza.color == color:
                    rey_pos = pieza.pos
        for pieza in piezas:
            if pieza.color != color:
                for cuadricula in pieza.atacando_cuadriculas(self):
                    if cuadricula.pos == rey_pos:
                        output = True
        if cambio_del_tablero is not None:
            if vieja_cuadricula is not None:
                vieja_cuadricula.ocupando_espacio = pieza_cambiante
            if nueva_cuadricula is not None:
                nueva_cuadricula.ocupando_espacio = nueva_cuadricula_vieja_pieza
        return output

    # Checkeamos si esta en jaque mate
    def esta_en_jaque_mate(self, color):
        output = False
        # Buscar el rey del color dado
        rey = None
        for cuadricula in self.cuadriculas:
            if (
                cuadricula.ocupando_espacio is not None
                and cuadricula.ocupando_espacio.color == color
                and isinstance(cuadricula.ocupando_espacio, Rey)
            ):
                rey = cuadricula.ocupando_espacio
            break

        if rey is None:
            return output

        for pieza in [i.ocupando_espacio for i in self.cuadriculas]:
            if pieza != None:
                if pieza.notacion == "R" and pieza.color == color:
                    rey = pieza

        if rey.get_movimientos_validos(self) == []:
            if self.esta_en_jaque(color):
                output = True

        return output

    # Resaltamos todos los posibles movimientos para una pieza en nuestro turno
    def dibujar(self, display):
        if self.pieza_seleccionada is not None:
            self.get_cuadricula_desde_pos(self.pieza_seleccionada.pos).resaltado = True
            for cuadricula in self.pieza_seleccionada.get_movimientos_validos(self):
                cuadricula.resaltado = True
        for cuadricula in self.cuadriculas:
            cuadricula.dibujar(display)

    def guardar_estado(self):
        estado = {
            "ancho": self.ancho,
            "alto": self.alto,
            "tile_ancho": self.tile_ancho,
            "tile_alto": self.tile_alto,
            "piezas": [],
        }

        for cuadricula in self.cuadriculas:
            pieza = cuadricula.ocupando_espacio
            if pieza is not None:
                estado["piezas"].append(
                    {
                        "pos": pieza.pos,
                        "color": pieza.color,
                        "tipo": type(pieza).__name__,
                    }
                )

        with open("data/autoguardado.json", "w") as file:
            json.dump(estado, file)

    def cargar_estado(self):
        with open("data/autoguardado.json", "r") as file:
            estado = json.load(file)

            self.ancho = estado["ancho"]
            self.alto = estado["alto"]
            self.tile_ancho = estado["tile_ancho"]
            self.tile_alto = estado["tile_alto"]
            if "config" in estado:
                self.config = estado["config"]
                self.cuadriculas = self.generar_cuadriculas()

            for pieza_data in estado["piezas"]:
                pieza_class = eval(pieza_data["tipo"])
                pieza = pieza_class(pieza_data["pos"], pieza_data["color"], self)
                cuadricula = self.get_cuadricula_desde_pos(pieza_data["pos"])
                cuadricula.ocupando_espacio = pieza

    def reiniciar_tablero(self):
        self.pieza_seleccionada = None
        self.turno = "white"
        self.config = [
            ["bT", "bC", "bA", "bQ", "bR", "bA", "bC", "bT"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wT", "wC", "wA", "wQ", "wR", "wA", "wC", "wT"],
        ]
        self.cuadriculas = self.generar_cuadriculas()
        self.setup_tablero()

    def realizar_movimiento_bot(self):
        # Obtener todas las cuadrículas disponibles para el color del turno actual
        cuadriculas_disponibles = []
        for cuadricula in self.cuadriculas:
            if cuadricula.ocupando_espacio is not None and cuadricula.ocupando_espacio.color == self.turno:
                cuadriculas_disponibles.append(cuadricula)

        if cuadriculas_disponibles:
            # Seleccionar una cuadrícula aleatoria
            cuadricula_origen = random.choice(cuadriculas_disponibles)
            pieza = cuadricula_origen.ocupando_espacio

            # Obtener los movimientos válidos de la pieza
            movimientos_validos = pieza.get_movimientos_validos(self)

            if movimientos_validos:
                # Seleccionar un movimiento aleatorio
                cuadricula_destino = random.choice(movimientos_validos)

                # Mover la pieza a la cuadrícula destino
                pieza.mover(self, cuadricula_destino)
                self.guardar_estado()
                self.turno = 'white' if self.turno == 'black' else 'black'
