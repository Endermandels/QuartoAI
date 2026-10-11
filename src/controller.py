from __future__ import annotations
from global_defs.state import *
from model import Model
from view import View
from agent import Agent
from time import perf_counter
from random import random

class Controller:
    def __init__(self, mdl: Model, vw: View, p1: Agent, p2: Agent, ngames: int):
        self.NGAMES: int = ngames
        self.running: bool = False
        self.mdl: Model = mdl
        self.vw: View = vw
        self.p1: Agent = p1
        self.p2: Agent = p2
        self.ngames: int = 0
        self.CHANCE_TO_SWITCH_PLAYERS = 0.5

    def update(self) -> None:
        if self.mdl.winner != Winner.NONE:
            self.vw.display_winner(self.mdl)
            self.p1.update_stats(self.mdl)
            self.p2.update_stats(self.mdl)
            self.mdl.reset()
            self.ngames += 1
            if random() < self.CHANCE_TO_SWITCH_PLAYERS:
                self._switch_players()
            return
    
        if self.mdl.is_give_phase(self.mdl.state):
            if self.mdl.is_p1_turn(self.mdl.state):
                self.mdl.give_piece(self.mdl.state, self.p1.query_give_piece(self.mdl))
            else:
                self.mdl.give_piece(self.mdl.state, self.p2.query_give_piece(self.mdl))
        else:
            if self.mdl.is_p1_turn(self.mdl.state):
                self.mdl.place_piece(self.mdl.state, self.p1.query_place_piece(self.mdl))
            else:
                self.mdl.place_piece(self.mdl.state, self.p2.query_place_piece(self.mdl))
            
        self.vw.update(self.mdl)
        
        if self.vw.quit_input:
            self.running = False
            return
        
    def run(self) -> None:
        # start_time: float = perf_counter()
        self.running = True
        
        while self.running and self.ngames < self.NGAMES:
            self.update()
            
            # # Catch unusually long hangs
            # if perf_counter() - start_time > 5:
            #     print("Hung up")
            #     self.running = False
    
    def _switch_players(self) -> None:
        temp: Agent = self.p1
        self.p1 = self.p2
        self.p2 = temp
        self.p1.set_player(True)
        self.p2.set_player(False)