from __future__ import annotations
from global_defs.state import PieceGive, Winner
from model import Model
from view import View
from agent import Agent
from time import perf_counter

class Controller:
    def __init__(self, mdl: Model, vw: View, p1: Agent, p2: Agent):
        self.running: bool = False
        self.mdl: Model = mdl
        self.vw: View = vw
        self.p1: Agent = p1
        self.p2: Agent = p2
    
    def _update_agent_stats(self) -> None:
        winner: Winner = self.mdl.check_winner(self.mdl.state)
        
        if winner == Winner.PLAYER_1:
            self.p1.stats.games_won += 1
            self.p2.stats.games_lost += 1
        elif winner == Winner.PLAYER_2:
            self.p2.stats.games_won += 1
            self.p1.stats.games_lost += 1
        else:
            self.p1.stats.games_tied += 1
            self.p2.stats.games_tied += 1
            
        self.p1.stats.games_played += 1
        self.p2.stats.games_played += 1

    def update(self) -> None:
        winner: Winner = self.mdl.check_winner(self.mdl.state)
        
        if winner != Winner.NONE:
            self.vw.display_winner(self.mdl)
            self._update_agent_stats()
            self.running = False
            return
        elif self.mdl.state.given_piece == PieceGive.EMPTY:
            if self.mdl.is_p1_turn(self.mdl.state):
                self.mdl.give_piece(self.mdl.state, self.p1.query_give_piece(self.mdl))
            else:
                self.mdl.give_piece(self.mdl.state, self.p2.query_give_piece(self.mdl))
        elif self.mdl.state.given_piece != PieceGive.EMPTY:
            if self.mdl.is_p1_turn(self.mdl.state):
                self.mdl.place_piece(self.mdl.state, self.p1.query_place_piece(self.mdl))
            else:
                self.mdl.place_piece(self.mdl.state, self.p2.query_place_piece(self.mdl))
            
        self.vw.update(self.mdl)
        
        if self.vw.quit_input:
            self.running = False
            return
        
    def run(self) -> None:
        start_time: float = perf_counter()
        self.running = True
        
        while (self.running):
            self.update()
            
            # Catch unusually long hangs
            # if perf_counter() - start_time > 5:
            #     print("Hung up")
            #     self.running = False