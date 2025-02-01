import pygame
from board import Board

class Agent:
    def __init__(self):
        self._init()
    
    def update(self):
        pass

    def _init(self):#privet no one else can call this
        self.selected = None
        self.board = Board()
        self.valid_moves = {}

    def select(self, row, col):#will determine wether or not we should move
        # select(row, col)
        if self.selected == None:
            selection = self.board.get_piece(row, col)
            if selection != 0:
                self.selected = selection
                self.valid_moves = self.board.get_valid_moves(self.selected)

                print(f"Piece({row},{col}) Content[{self.selected}]")
                self.selected = None
                return self.valid_moves
        
        return 'Agent: No piece selected'
        
    def setBoard(self, board, whites, blacks):

        self.board.setBoard(board)
        self.board.setBlack(blacks)
        self.board.setWhite(whites)

        

        
