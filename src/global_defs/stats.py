from __future__ import annotations

class Stats:
    def __init__(self, agent_name: str = "DEFAULT"):
        self.agent_name: str = agent_name
        self.games_won: int = 0
        self.games_lost: int = 0
        self.games_tied: int = 0
        self.games_played: int = 0
    
    def __repr__(self):
        return (f">>> Agent: \t\t{self.agent_name}\n" \
                + f">>> Games Won: \t\t{self.games_won}\n" \
                + f">>> Games Lost: \t{self.games_lost}\n" \
                + f">>> Games Tied: \t{self.games_tied}\n" \
                + f">>> Games Played: \t{self.games_played}\n")
    
    def duplicate(self) -> Stats:
        return Stats(self.agent_name)

class QLearnStats(Stats):
    def __init__(self, agent_name = "DEFAULT"):
        super().__init__(agent_name)
        self.q_table_hits: int = 0
        self.q_table_lookups: int = 0
    
    def __repr__(self):
        return (super().__repr__() \
                + f">>> Hit Rate: \t{self.q_table_hits / self.q_table_lookups}")
    
    def duplicate(self) -> Stats:
        return QLearnStats(self.agent_name)