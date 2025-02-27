import pygame
from board import Board
from copy import deepcopy

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
        selection = None
        if self.selected == None:
            selection = self.board.get_piece(row, col)
            if selection != 0 and selection.team == self.turn: # selection.team == self.turn
                self.selected = selection
                self.valid_moves = self.board.get_valid_moves(self.selected)

                if self.valid_moves == {}:
                    self.selected = None
                    return 'Agent: Piece can\'t move'
                
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
            self.change_turn()
        else:
            return False
        
        return True
    
    def ia_move(self, team):
        best_moves_for_pieces = {}

        for piece in self.board.get_all_team_pieces(team):
            possible_moves = self.board.get_valid_moves(piece)

            moves_with_rewards = {
                move[0]: sum(1 if skipped.team != team else -1 for skipped in move[1])
                for move in possible_moves.items()
            }

            best_move_for_piece = max(moves_with_rewards.items(), key=lambda item: item[1], default=None)
            if best_move_for_piece is not None:
                best_moves_for_pieces[(piece.team, (piece.row, piece.col))] = best_move_for_piece

        return next(iter(sorted(best_moves_for_pieces.items(), key=lambda item: item[1][1], reverse=True)), None)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'black':
            self.turn = 'white'
        else:
            # best_piece_move = self.ia_move('black')
            # print(f"Result Best piece move: {best_piece_move}")
            self.turn = 'black' 
        
    def setBoard(self, board, whites, blacks):

        self.board.setBoard(board)
        self.board.setBlack(blacks)
        self.board.setWhite(whites)

    def algo(self, initial_position):
        best_move = None
        maxEval = initial_evaluation = len(initial_position.get_all_team_pieces('black')) - len(initial_position.get_all_team_pieces('white'))

        for move, piece, final_position in self.get_all_moves(initial_position, 'black'):
            black_evaluation = len(move.get_all_team_pieces('black')) - len(move.get_all_team_pieces('white'))

            maxEval = max(black_evaluation, initial_evaluation)

            initial_evaluation = maxEval
            if maxEval == black_evaluation:
                best_move = move, piece, final_position

        return best_move # move, piece, final_position

    def simulate_move(self, pice, move, board, skip):
        board.move(pice, move[0], move[1])
        if skip:
            board.remove(skip)

        return board

    def get_all_moves(self, board, color):
        moves = [] #[(board, initial_piece, final_position)]

        for piece in board.get_all_team_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            #(row, col): [pieces]
            for move, skip in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append((new_board, piece, move))

        return moves

        

        
