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

    def expand_initial_node_moves(self, initial_nodes, color, minmax):
        nodes = self.get_all_moves(initial_nodes, color)
        for node in nodes:
            new_board, _, _, _, _, _ = node
            minmax[new_board] = {"node": node, "cost" : self.cost(new_board), "nodes": {}}
        return nodes

    def expand_moves_for_nodes(self, initial_nodes, color, minmax, startOppMoves=False):
        moves_after_expansion =  [] # [(move, piece, final_position)]

        if startOppMoves:
            for move, piece, final_position, opp_piece, opp_final, nodes in initial_nodes:
                parent_data = minmax[move]

                moves = self.get_all_moves(move, color)
                for node_data in moves:
                    my_move, _ , _, _, _, _ = node_data
                    node = (my_move, piece, final_position, opp_piece, opp_final, [])
                    nodes.append(node)
                    parent_data["nodes"][my_move] = {"node": node, "cost" : self.cost(my_move), "nodes": {}}
                    moves_after_expansion.append(node)
                self.oppturn_moves = initial_nodes

        else:
            for node_data in initial_nodes:
                move, piece, final_position, _, _, nodes = node_data
                parent_data = minmax[move]
                moves = self.get_all_moves(move, color)
                for my_move, opp_piece, opp_final, _, _, _ in moves:
                    node_expand = (my_move, piece, final_position, opp_piece, opp_final, [])
                    parent_data["nodes"][my_move] = {"node": node_expand, "cost" : self.cost(my_move) * -1 , "nodes": {}}
                    moves_after_expansion.append(node_expand)

        return moves_after_expansion

    def cost(self, board):
        return len(board.get_all_team_pieces('black')) - len(board.get_all_team_pieces('white'))

    def evaluate_best_move(self, possible_moves, minmax):
        first_max_ev = float('-inf')
        first_player_best_move = None

        for value in minmax.values():
            first_cost = value['cost']
            first_max_ev = max(first_cost, first_max_ev)

            if first_max_ev == first_cost:
                first_player_best_move = value['node']

        
        best_move = None
        max_eval = float('-inf')  # Initialize to negative infinity

        for move_data in possible_moves:
            move, piece, final_state, _, _, _ = move_data
            evaluation = len(move.get_all_team_pieces('black')) - len(move.get_all_team_pieces('white'))

            max_eval = max(evaluation, max_eval)

            if max_eval == evaluation:
                best_move = move_data

        move, piece, final_state, _, _, _ = best_move 

        return first_player_best_move[0], first_player_best_move[1], first_player_best_move[2]

    def algo(self, initial_position, opp_start, opp_final):

        best_move = None
        moves_after_expansion =  [] 
        minmax = {}

        if self.oppturn_moves is not None:
            possible_moves_from_root = next(
                (nodes for _, _, _, piece_, final_position, nodes in self.oppturn_moves 
                if (piece_.row, piece_.col) == opp_start and final_position == opp_final), 
                None
            )

        possible_moves_from_root = self.expand_initial_node_moves(initial_position, 'black', minmax) # [(move, piece_b, final_position, None, None, [])]

        moves_after_expansion = self.expand_moves_for_nodes(possible_moves_from_root, 'white', minmax) # [(move, piece_b, final_position, opp, oppfinal, [])]

        finish = {
            move: data
            for value in minmax.values()
            for move, data in value['nodes'].items()
        }
        moves_after_expansion = self.expand_moves_for_nodes(moves_after_expansion, 'black', finish , True) # [(move, piece_b, final_position, opp, oppfinal, [])]
        #Evaluation

        best_move = self.evaluate_best_move(moves_after_expansion, minmax)

        return best_move # move, piece, 

    def simulate_move(self, pice, move, board, skip):
        if skip:
            board.remove(skip)
        board.move(pice, move[0], move[1])

        return board

    def get_all_moves(self, board, color):
        moves = [] #[(board, initial_piece, final_position)]
        
        for piece in board.get_all_team_pieces(color):
            valid_moves = board.get_valid_moves(piece) #{(row, col): [pieces]}
            result = []
            maximal_elimination_moves = []
            
            for item in valid_moves.items(): #((row, col): [pieces])
                skipped = item[1]
                if skipped and all(skipped_piece.team != piece.team for skipped_piece in skipped):
                    result.append(item)
            if not result:
                maximal_elimination_moves = [item for item in valid_moves.items()][:1]
            else:
                maximal_elimination_moves = result


            for move, skip in maximal_elimination_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append((new_board, piece, move, None, None, []))
        moves.reverse()
        return moves

        

        
