import pygame

class Pieza:
    def __init__(self, pos, color, tablero):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.se_ha_movido = False