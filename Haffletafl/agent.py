import pygame
from board import Board

class Agent:
    def __init__(self):
        self._init()
        self.selected = None

    def update(self):
        pass

    def _init(self):#privet no one else can call this
        self.selected = None
        self.board = Board()
        self.valid_moves = {} 

        
    def setBoard(self, board, whites, blacks):

        self.board.setBoard(board)
        self.board.setBlack(blacks)
        self.board.setWhite(whites)

        


    def select(self, row, col):#will determine wether or not we should move
        # select(row, col)
        if self.selected == None:
            self.selected = self.board.get_piece(row, col)
            if self.selected != 0:
                self.valid_moves = self.board.get_valid_moves(self.selected)

            print(f"Piece({row},{col}) Content[{self.selected}]")
            return self.valid_moves
        else:
            self._move(row, col)
            self.selected = None

            

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
        else:
            return False
        
        return True
    
  

    def get_board(self):
        # Definir el ancho de las celdas
        cell_width = 8  # Ajusta el valor según sea necesario para que todos los valores encajen
        
        for i in range(11):
            row = []  # Lista para almacenar las piezas de la fila
            for j in range(11):
                piece = self.board.get_piece(i, j)
                car = ''
                if piece == 0:  # Si la pieza es "0", la reemplazamos por un espacio vacío
                    car = " "  # O puedes usar otro marcador si lo prefieres
                if piece != 0:
                    car = piece.team
                # Añadir la pieza al listado de la fila con el formato adecuado (ancho fijo)
                row.append(f"{car: <{cell_width}}")  # Alineamos a la izquierda y usamos el ancho definido

            # Imprimir la fila uniendo las celdas
            print("".join(row))
        
