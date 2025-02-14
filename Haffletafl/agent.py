import pygame
from board import Board

class Agent:
    def __init__(self, team = 'white'):
        self._init()
        self.turn = team
    
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
            if selection != 0: # selection.team == self.turn
                self.selected = selection
                self.valid_moves = self.board.get_valid_moves(self.selected)

                if self.valid_moves == {}:
                    self.selected = None
                    return 'Agent: Piece can\'t move'
                
                self.selected = None
                #print(f"Selected Piece({row},{col}) Content[{self.selected}]")
                
                return self.valid_moves
            
            return 'Agent: Incorrect Pice Selected'

        else:
            # If a piece is selected, attempt to make the move
            result = self._move(row, col)
            if result:
                #Move was successful: change turn and reset the selection
                self.valid_moves = {}
                self.selected = None

                return 'Agent: successful: change turn and reset'

            else:
                # # Move was unsuccessful: reset and reselect the piece
                self.valid_moves = {}
                self.selected = None

                return 'Agent: unsuccessful: reset and reselect'

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
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'black':
            self.turn = 'white'
        else:
            self.turn = 'black' 
        
    def setBoard(self, board, whites, blacks):

        self.board.setBoard(board)
        self.board.setBlack(blacks)
        self.board.setWhite(whites)

        

        
