from __future__ import annotations
from global_defs.state import PieceMask, ActionGive, ActionPlace, WHITE_PIECES, BLACK_PIECES
from global_defs.stats import Stats
from model import Model
from view import View
from random import choice

class Agent:
    def __init__(self, is_p1: bool, stats: Stats):
        self.is_p1: bool = is_p1
        self.stats: Stats = stats

    def query_give_piece(self, mdl: Model) -> ActionGive | None:
        return None

    def query_place_piece(self, mdl: Model) -> ActionPlace | None:
        return None

class HumanAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats, vw: View):
        super().__init__(is_p1, stats)
        self.vw: View = vw
    
    def query_give_piece(self, mdl: Model) -> ActionGive | None:
        return self.vw.query_give_piece(mdl)

    def query_place_piece(self, mdl: Model) -> ActionPlace | None:
        return self.vw.query_place_piece(mdl)

class RandomAgent(Agent):
    def __init__(self, is_p1: bool, stats: Stats):
        super().__init__(is_p1, stats)
    
    def query_give_piece(self, mdl: Model) -> ActionGive | None:
        bit_mask_pieces: list[int]
        agent_pieces: int = WHITE_PIECES if self.is_p1 else BLACK_PIECES
        agent_pieces &= mdl.state.remaining_pieces
        
        bit_mask_pieces = [1 << i for i in range(agent_pieces.bit_length()) if ((agent_pieces >> i) & 1) == 1]
        
        return ActionGive(choice(bit_mask_pieces))

    def query_place_piece(self, mdl: Model) -> ActionPlace | None:
        available_coords: list[tuple[int, int]] = []
        chosen_coords: tuple[int, int]
        
        for r in range(len(mdl.state.board)):
            for c, piece in enumerate(mdl.state.board[r]):
                if piece == PieceMask.EMPTY:
                    available_coords.append((r, c))
  
        chosen_coords = choice(available_coords)
        
        return ActionPlace(chosen_coords[0], chosen_coords[1])