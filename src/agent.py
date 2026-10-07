from __future__ import annotations
from global_defs.state import State, Winner, Action, PiecePlace, PieceGive
from global_defs.stats import Stats
from collections import defaultdict
from model import Model
from view import View
from random import choice

class Agent:
    def __init__(self, is_p1: bool, stats: Stats):
        self.is_p1: bool = is_p1
        self.stats: Stats = stats

    def query_give_piece(self, mdl: Model) -> Action | None:
        return None

    def query_place_piece(self, mdl: Model) -> Action | None:
        return None

class HumanAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats, vw: View):
        super().__init__(is_p1, stats)
        self.vw: View = vw
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        return self.vw.query_give_piece(mdl)

    def query_place_piece(self, mdl: Model) -> Action | None:
        return self.vw.query_place_piece(mdl)

class RandomAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats):
        super().__init__(is_p1, stats)
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        return Action(piece=choice(mdl.legal_give_actions(mdl.state)))

    def query_place_piece(self, mdl: Model) -> Action | None:
        return Action(board_coords=choice(mdl.legal_place_actions(mdl.state)))

class HeuristicAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats):
        super().__init__(is_p1, stats)
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        # Never give a winning piece, if possible
        
        # For each piece left,
        #  check if any spot on the board having that piece will result in a win for the opponent
        #  if there are any spots, don't give that piece
        # If after searching no pieces are left that won't result in defeat, choose a random piece
        
        legal_pieces: list[int] = mdl.legal_give_actions(mdl.state)
        good_pieces: list[int] = []
        
        for piece in legal_pieces:
            bad_piece: bool = False
            piece_place: int = PiecePlace[PieceGive(piece).name].value
            
            for r in range(len(mdl.state.board)):
                for c in range(len(mdl.state.board[r])):
                    if mdl.check_winner(mdl.state, r, c, piece_place) == (Winner.PLAYER_2 if self.is_p1 else Winner.PLAYER_1):
                        bad_piece = True
                        break
            
            if not bad_piece:
                good_pieces.append(piece)
            
        return Action(piece=choice(good_pieces if len(good_pieces) > 0 else legal_pieces)) 

    def query_place_piece(self, mdl: Model) -> Action | None:
        # Always place piece in a winning spot, if possible
        
        # For each place,
        #  check if placing the piece results in a win
        #  if there are any spots, place it there
        # Otherwise, place it randomly
        
        legal_spaces: list[tuple[int, int]] = mdl.legal_place_actions(mdl.state)
        winning_space: tuple[int, int] | None = None
        piece_place: int = PiecePlace[PieceGive(mdl.state.given_piece).name].value
        
        for space in legal_spaces:
            if mdl.check_winner(mdl.state, space[0], space[1], piece_place) == (Winner.PLAYER_1 if self.is_p1 else Winner.PLAYER_2):
                winning_space = space
                break
        
        return Action(board_coords=(winning_space if winning_space != None else choice(legal_spaces)))
    
class QLearnAgent(Agent):
    # store q values: {(state, action): -> q}
    # store epsilon (exploration rate)
    # store alpha (learning rate)
    # store gamma (discount)
    
    # update q values: Q(s, a) = Q(s, a) + alpha * (R(s) + gamma * max(Q(s', a')) - Q(s, a))
    # where Q(s', a') is the q value of the next state given the next action
    # the update rule uses back propogation, so the next state is actually the current state
    
    def __init__(self, is_p1, stats, epsilon: int = 0.5, alpha: int = 0.5, gamma: int = 0.5):
        super().__init__(is_p1, stats)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        
        self.q_table = defaultdict(float) # default q of 0; populate q as agent encounters state, action pairs
    
    def _update_q_table(self, state: State, action: Action) -> None:
        """ Update q table based on observation of what state the given action produced """
        pass
    