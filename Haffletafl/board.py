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
        left = Direction(-direction.y, direction.x)
        right = Direction(direction.y, -direction.x)
        current_position = (start[0] + direction.x, start[1] + direction.y)
        
        if self.is_out_of_bounds(current_position):
            return moves
        current_piece = self.get_piece(current_position[0], current_position[1])
        if current_piece == 0:
            eliminate_left = self.try_to_eliminate_enemy(current_position, left, team)
            eliminate_forward = self.try_to_eliminate_enemy(current_position, direction, team)
            eliminate_right = self.try_to_eliminate_enemy(current_position, right, team)
            self.union_dicts(moves, eliminate_left)
            self.union_dicts(moves, eliminate_forward)
            self.union_dicts(moves, eliminate_right)
            
            # eliminate_myself = self.dangerous_position(current_position, left, right, team)
            # self.union_dicts(moves, eliminate_myself)
            
            moves.update(self.scan_direction_for_moves(current_position, direction, team))
        elif current_piece.team == team:
            return moves
        else:
            return moves


        return moves
    
    def union_dicts(self, dict1, dict2):
        for key, value in dict2.items():
            if key in dict1:
                dict1[key].extend(value)  
            else:
                dict1[key] = value

    
    def dangerous_position(self, initial_position: tuple, left: Direction, right: Direction, team):
        kill_myself = {} # (1, 1) = {[Piece]}
        kill_myself[initial_position] = []
        current_piece = self.get_piece(initial_position[0], initial_position[1])
        left_position = (initial_position[0] + left.x, initial_position[1] + left.y)
        right_position = (initial_position[0] + right.x, initial_position[1] + right.y)

        if self.is_out_of_bounds(left_position) and not self.is_out_of_bounds(right_position): 
            right_piece = self.get_piece(right_position[0], right_position[1])
            if right_piece == 0:
                pass
            elif right_piece.team !=  team:
                kill_myself[initial_position] = [current_piece]
        elif self.is_out_of_bounds(right_position) and not self.is_out_of_bounds(left_position): 
            left_piece = self.get_piece(left_position[0], left_position[1])
            if left_piece == 0:
                pass
            elif left_piece.team !=  team:
                kill_myself[initial_position] = [current_piece]
        elif not self.is_out_of_bounds(right_position) and not self.is_out_of_bounds(left_position):
            left_piece = self.get_piece(left_position[0], left_position[1])
            right_piece = self.get_piece(right_position[0], right_position[1])
            if left_piece != 0 and right_piece != 0:
                if left_piece.team != team and right_piece.team != team: 
                    kill_myself[initial_position] = [current_piece]
        
        return kill_myself

    def try_to_eliminate_enemy(self, initial_position: tuple, direction: Direction, team):
        elimination_list = {} # (1, 2) = {[Piece]}
        elimination_list[initial_position] = []
        current_position = (initial_position[0] + direction.x, initial_position[1] + direction.y)
        opposite_position = (initial_position[0] - direction.x, initial_position[1] - direction.y)

        if self.is_out_of_bounds(current_position):
            if not self.is_out_of_bounds(opposite_position):
                opposite_piece = self.get_piece(opposite_position[0], opposite_position[1])
                if opposite_piece != 0 and opposite_piece.team != team: 
                    elimination_list[initial_position] = [self.get_piece(initial_position[0], initial_position[1])]                
                
            return elimination_list # either {[]} or {[Initial Piece]}

        current_piece = self.get_piece(current_position[0], current_position[1])
        
        if current_piece == 0:
            return elimination_list
        elif current_piece.team == team:
            return elimination_list
        else:
            next_position = (current_position[0] + direction.x, current_position[1] + direction.y)
            if self.is_out_of_bounds(next_position):
                elimination_list[initial_position] = [current_piece]

                return elimination_list
            
            next_piece = self.get_piece(next_position[0], next_position[1])
            
            if next_piece == 0:
                return elimination_list
            if next_piece.team == team:
                elimination_list[initial_position] = [current_piece]
            else:
                pass

        return elimination_list  # (1, 2) = {[(1,3)]}

    def is_out_of_bounds(self, position: tuple):
        # Assuming the board size is 12x12, adjusting the bounds check
        return position[0] < 0 or position[0] >= 11 or position[1] < 0 or position[1] >= 11 