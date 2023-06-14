import pickle
import os
import pygame
from data.clases.cuadricula import Cuadricula
from data.clases.piezas.torre import Torre
from data.clases.piezas.alfil import Alfil
from data.clases.piezas.peon import Peon
from data.clases.piezas.rey import Rey
from data.clases.piezas.reina import Reina
from data.clases.piezas.caballo import Caballo

ARCHIVO_GUARDADO = "autoguardado.pickle"

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
            ['bT', 'bC', 'bA', 'bQ', 'bR', 'bA', 'bC', 'bT'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wT', 'wC', 'wA', 'wQ', 'wR', 'wA', 'wC', 'wT'],
        ]
        self.cuadriculas = self.generar_cuadriculas()
        self.setup_tablero()

#Generamos las cuadriculas en el tablero
    def generar_cuadriculas(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Cuadricula(x,  y, self.tile_ancho, self.tile_alto)
                )
        return output

    def get_cuadricula_desde_pos(self, pos):
        for cuadricula in self.cuadriculas:
            if (cuadricula.x, cuadricula.y) == (pos[0], pos[1]):
                return cuadricula

    def get_pieza_desde_pos(self, pos):
        return self.get_cuadricula_desde_pos(pos).ocupando_espacio

#Seteamos el tablero con su correspondiente pieza
    def setup_tablero(self):
        cuadriculas = []
        for y, fila in enumerate(self.config):
            for x, pieza in enumerate(fila):
                if pieza != '':
                    cuadricula = self.get_cuadricula_desde_pos((x, y))
                    #Miramos dentro del contenido a ver que pieza corresponde
                    if pieza[1] == 'T':
                        cuadricula.ocupando_espacio = Torre(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    elif pieza[1] == 'C':
                        cuadricula.ocupando_espacio = Caballo(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    elif pieza[1] == 'A':
                        cuadricula.ocupando_espacio = Alfil(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    elif pieza[1] == 'Q':
                        cuadricula.ocupando_espacio = Reina(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    elif pieza[1] == 'R':
                        cuadricula.ocupando_espacio = Rey(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    elif pieza[1] == 'P':
                        cuadricula.ocupando_espacio = Peon(
                            (x, y), 'white' if pieza[0] == 'w' else 'black', self
                        )
                    cuadriculas.append(cuadricula)
        return cuadriculas


    def obtener_cuadriculas_info(self):
        cuadriculas_info = []
        for cuadricula in self.cuadriculas:
            info = {
                "pos": cuadricula.pos,
                "x": cuadricula.x,
                "y": cuadricula.y,
                "pieza": None
            }
        if cuadricula.ocupando_espacio is not None:
            info["pieza"] = cuadricula.ocupando_espacio.obtener_informacion()
            cuadriculas_info.append(info)
        return cuadriculas_info


    def crear_pieza_desde_informacion(info, tablero):
        pos = info["pos"]
        color = info["color"]
        tipo = info["tipo"]
        
        if tipo == "Torre":
            return Torre(pos, color, tablero)
        elif tipo == "Caballo":
            return Caballo(pos, color, tablero)
        elif tipo == "Alfil":
            return Alfil(pos, color, tablero)
        elif tipo == "Reina":
            return Reina(pos, color, tablero)
        elif tipo == "Rey":
            return Rey(pos, color, tablero)
        elif tipo == "Peon":
            return Peon(pos, color, tablero)

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
            self.guardar_estado()
        elif cuadricula_clickeada.ocupando_espacio is not None:
            if cuadricula_clickeada.ocupando_espacio.color == self.turno:
                self.pieza_seleccionada = cuadricula_clickeada.ocupando_espacio

#Checkeamos si el jugador está en jaque
    def esta_en_jaque(self, color, cambio_del_tablero=None): # cambio_del_tablero = [(x1, y1), (x2, y2)]
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
                    vieja_cuadricula.ocupando_espacio = None
            for cuadricula in self.cuadriculas:
                if cuadricula.pos == cambio_del_tablero[1]:
                    nueva_cuadricula = cuadricula
                    nueva_cuadricula_vieja_pieza = nueva_cuadricula.ocupando_espacio
                    nueva_cuadricula.ocupando_espacio = pieza_cambiante
        piezas = [
            i.ocupando_espacio for i in self.cuadriculas if i.ocupando_espacio is not None
        ]
        if pieza_cambiante is not None:
            if pieza_cambiante.notacion == 'R':
                rey_pos = nueva_cuadricula.pos
        if rey_pos == None:
            for pieza in piezas:
                if pieza.notacion == 'R' and pieza.color == color:
                        rey_pos = pieza.pos
        for pieza in piezas:
            if pieza.color != color:
                for cuadricula in pieza.atacando_cuadriculas(self):
                    if cuadricula.pos == rey_pos:
                        output = True
        if cambio_del_tablero is not None:
            vieja_cuadricula.ocupando_espacio = pieza_cambiante
            nueva_cuadricula.ocupando_espacio = nueva_cuadricula_vieja_pieza
        return output

#Checkeamos si esta en jaque mate
    def esta_en_jaque_mate(self, color):
        output = False
        # Buscar el rey del color dado
        rey = None
        for cuadricula in self.cuadriculas:
            if cuadricula.ocupando_espacio is not None and cuadricula.ocupando_espacio.color == color and isinstance(cuadricula.ocupando_espacio, Rey):
                rey = cuadricula.ocupando_espacio
            break

        if rey is None:
            return output

        for pieza in [i.ocupando_espacio for i in self.cuadriculas]:
            if pieza != None:
                if pieza.notacion == 'R' and pieza.color == color:
                    rey = pieza

        if rey.get_movimientos_validos(self) == []:
            if self.esta_en_jaque(color):
                output = True

        return output

#Resaltamos todos los posibles movimientos para una pieza en nuestro turno
    def dibujar(self, display):
        if self.pieza_seleccionada is not None:
            self.get_cuadricula_desde_pos(self.pieza_seleccionada.pos).resaltado = True
            for cuadricula in self.pieza_seleccionada.get_movimientos_validos(self):
                cuadricula.resaltado = True
        for cuadricula in self.cuadriculas:
            cuadricula.dibujar(display)


    def guardar_estado(self):
        cuadriculas_info = self.obtener_cuadriculas_info()
        estado = {
            "ancho": self.ancho, 
            "alto": self.alto,
            "tile_ancho": self.tile_ancho,
            "tile_alto": self.tile_alto,
            "pieza_seleccionada": self.pieza_seleccionada,
            "turno": self.turno,
            "config": self.config,
            "cuadriculas": cuadriculas_info
            # Otros datos relevantes del tablero que desees guardar
        }

        with open("data/autoguardado.pickle", "wb") as file:
            pickle.dump(estado, file)


    def cargar_estado(self):
        # Cargar el estado desde el archivo utilizando pickle
        with open("data/autoguardado.pickle", "rb") as file:
            estado = pickle.load(file)

        # Restaurar el estado del tablero
        self.ancho = estado["ancho"]
        self.alto = estado["alto"]
        self.tile_ancho = estado["tile_ancho"]
        self.tile_alto = estado["tile_alto"]
        self.pieza_seleccionada = estado["pieza_seleccionada"]
        self.turno = estado["turno"]
        self.config = estado["config"]
        cuadriculas_info = estado["cuadriculas"]
        for cuadricula_info in cuadriculas_info:
            cuadricula = self.get_cuadricula_desde_pos(cuadricula_info["pos"])
            cuadricula.ocupando_espacio = self.crear_pieza_desde_informacion(cuadricula_info["pieza"])