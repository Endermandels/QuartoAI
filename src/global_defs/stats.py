class Stats:
    def __init__(self, agent_name: str = "DEFAULT"):
        self.agent_name: str = agent_name
        self.games_won: int = 0
        self.games_lost: int = 0
        self.games_tied: int = 0
        self.games_played: int = 0