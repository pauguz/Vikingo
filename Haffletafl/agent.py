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
        self.oppturn_moves = None

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

    def expand_initial_node_moves(self, initial_node, color):
        
        return self.get_all_moves(initial_node, color)

    def expand_moves_for_nodes(self, initial_nodes, color, startOppMoves=False):
        moves_after_expansion =  [] # [(move, piece, final_position)]

        if startOppMoves:
            for move, piece, final_position, opp_piece, opp_final, nodes in initial_nodes:
                moves = self.expand_initial_node_moves(move, color)
                for my_move, _ , _ in moves:
                    node = (my_move, piece, final_position, opp_piece, opp_final, [])
                    nodes.append(node)
                    moves_after_expansion.append(node)
                self.oppturn_moves = initial_nodes

        else:
            for move, piece, final_position in initial_nodes:
                moves = self.expand_initial_node_moves(move, color)
                for my_move, opp_piece, opp_final in moves:
                    moves_after_expansion.append((my_move, piece, final_position, opp_piece, opp_final, []))

        return moves_after_expansion

    def evaluate_best_move(self, possible_moves):
        best_move = None
        max_eval = float('-inf')  # Initialize to negative infinity

        for move_data in possible_moves:
            move, piece, final_state, _, _, _ = move_data
            evaluation = len(move.get_all_team_pieces('black')) - len(move.get_all_team_pieces('white'))

            max_eval = max(evaluation, max_eval)

            if max_eval == evaluation:
                best_move = move_data

        move, piece, final_state, _, _, _ = best_move 
        self.oppturn_moves = next(
            (nodes for _, piece_, final_position, _, _, nodes in self.oppturn_moves 
            if piece_ == piece and final_position == final_state), 
            None
        )

        return move, piece, final_state

    def algo(self, initial_position, final, initial):

        best_move = None

        possible_moves_from_root = self.expand_initial_node_moves(initial_position, 'black') # [(move, piece_b, final_position)]

        moves_after_expansion =  [] 

        moves_after_expansion = self.expand_moves_for_nodes(possible_moves_from_root, 'white') # [(move, piece_b, final_position, opp, oppfinal, [])]
        
        moves_after_expansion = self.expand_moves_for_nodes(moves_after_expansion, 'black', True) # [(move, piece_b, final_position, opp, oppfinal, [])]
        #Evaluation

        best_move = self.evaluate_best_move(moves_after_expansion)

        return best_move # move, piece, 

    def simulate_move(self, pice, move, board, skip):
        if skip:
            board.remove(skip)
        board.move(pice, move[0], move[1])

        return board

    def get_all_moves(self, board, color):
        moves = [] #[(board, initial_piece, final_position)]

        for piece in board.get_all_team_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            #(row, col): [pieces]
            maximal_elimination_moves = sorted(
                valid_moves.items(),
                key=lambda item: sum(-1 if piece.team == color else 1 for piece in item[1]),
                reverse=True
            )[:1]
            for move, skip in maximal_elimination_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append((new_board, piece, move))
        moves.reverse()
        return moves

        

        
