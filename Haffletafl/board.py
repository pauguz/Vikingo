from piece import Piece

from collections import namedtuple
Direction = namedtuple('Direction', ['x', 'y'])

ROWS = 12
COLS = 12

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0

    def get_all_team_pieces(self, team):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.team == team:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def setBoard(self, board):
        self.board = board
    
    def setBlack(self, blacks):
        self.black_left = blacks
        
    def setWhite(self, whites):
        self.white_left = whites


    def _create_board(self): #Need pieces
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 1:
                    self.board[row].append(Piece(row, col, 'white'))
                elif row > ROWS - 1:
                    self.board[row].append(Piece(row, col, 'black'))
                else:
                    self.board[row].append(0)
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.team == 'black':
                    self.black_left -= 1
                else: 
                    self.white_left -= 1

    def get_valid_moves(self, piece):
        moves = {}#store the move, (4, 5): [(3,4)] and we have to remove that piece(3,4)
        directions = [
            Direction(1, 0),   # West
            Direction(-1, 0),  # East
            Direction(0, 1),   # North
            Direction(0, -1)   # South
        ] 

        position_start = (piece.row, piece.col)

        for direction in directions:
            moves.update(self.scan_direction_for_moves(position_start, direction, piece.team))
    
        return moves
 
    def scan_direction_for_moves(self, start: tuple, direction: Direction, team):
        moves = {}
        return moves