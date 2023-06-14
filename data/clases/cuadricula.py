import pygame

class Cuadricula:

    #Crea el cuadrado
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.abs_x = x * ancho
        self.abs_y = y * alto
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x,y)
        self.color = 'light' if (x+y) % 2 == 0 else 'dark'
        self.dibujar_color = (214, 199, 192) if self.color == 'light' else (53, 53, 53)
        self.resaltar_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
        self.ocupando_espacio = None
        self.coordenada = self.get_coordenada()
        self.resaltado = False
        self.cuadrado = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.ancho,
            self.alto,
        )

    #Obtener el nombre de la posición (por ej: A1)
    def get_coordenada(self):
        columnas = 'abcdefgh'
        return columnas[self.x] + str(self.y + 1)

    def dibujar(self, display):
        #Determina si un cuadrado es negro, blanco o está resaltado
        if self.resaltado:
            pygame.draw.rect(display, self.resaltar_color, self.cuadrado)
        else:
            pygame.draw.rect(display, self.dibujar_color, self.cuadrado)
        
        #Añade la pieza al cuadrado
        if self.ocupando_espacio != None:
            centrar_cuadrado = self.ocupando_espacio.img.get_rect()
            centrar_cuadrado.center = self.cuadrado.center
            display.blit(self.ocupando_espacio.img, centrar_cuadrado.topleft)