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
    
    def move(self, tablero, cuadricula, forzar=False):
        for i in tablero.squares:
            i.resaltado = False
        if cuadricula in self.get_movimientos_validos(tablero) or forzar:
            prev_cuadricula = tablero.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = cuadricula.pos, cuadricula.x, cuadricula.y
            prev_cuadricula.ocupando_espacio = None
            cuadricula.ocupando_espacio = self
            tablero.pieza_seleccionada = None
            self.se_ha_movido = True
            # Pawn promotion
            if self.notation == ' ':
                if self.y == 0 or self.y == 7:
                    from data.classes.pieces.Queen import Queen
                    square.occupying_piece = Queen(
                        (self.x, self.y),
                        self.color,
                        board
                    )
            # Move rook if king castles
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            return True
        else:
            board.selected_piece = None
            return False

    # True for all pieces except pawn
    def attacking_squares(self, board):
        return self.get_moves(board)