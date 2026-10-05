from __future__ import annotations
from global_defs.state import ActionGive, ActionPlace
from model import Model
from view import View

class Agent:
    def __init__(self):
        pass

    def query_give_piece(self, mdl: Model) -> ActionGive | None:
        return None

    def query_place_piece(self, mdl: Model) -> ActionPlace | None:
        return None

class Human(Agent):
    def __init__(self, vw: View):
        super().__init__()
        self.vw: View = vw
    
    def query_give_piece(self, mdl: Model) -> ActionGive | None:
        return self.vw.query_give_piece(mdl)

    def query_place_piece(self, mdl: Model) -> ActionPlace | None:
        return self.vw.query_place_piece(mdl)
    