from global_defs.stats import Stats
from controller import Controller
from view import View, TerminalView
from model import Model
from agent import HumanAgent, RandomAgent

RUNS: int = 50

def train(runs) -> None:
    vw = View()
    vwt = TerminalView()
    p1 = RandomAgent(True, Stats("Random 1"))
    p2 = RandomAgent(False, Stats("Random 2"))
    
    for i in range(runs):
        mdl = Model()
        ctrl = Controller(mdl, vw, p1, p2)
        ctrl.run()
    
    vwt.display_stats(p1.stats)
    vwt.display_stats(p2.stats)

def main() -> None:
    train(RUNS)

if __name__ == "__main__":
    main()