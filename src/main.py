from global_defs.stats import Stats
from controller import Controller
from view import View, TerminalView
from model import Model
from agent import HeuristicAgent, RandomAgent, HumanAgent, Agent
from time import perf_counter

RUNS: int = 1000

def train(runs) -> None:
    vw: View = View()
    vwt: View = TerminalView()
    p1: Agent = RandomAgent(True, Stats("Random 1"))
    # p2: Agent = HumanAgent(False, Stats("Human 2"), vwt)
    # p2: Agent = RandomAgent(False, Stats("Random 2"))
    p2: Agent = HeuristicAgent(False, Stats("Heuristic 2"))
    start_time: float = perf_counter()
    end_time: float
    
    for i in range(runs):
        mdl = Model()
        ctrl = Controller(mdl, vw, p1, p2)
        ctrl.run()
        # print(f"Game {i + 1} Completed")
        
    end_time = perf_counter()
    print(f"Runtime: {(end_time - start_time):.6f} seconds")
    
    vwt.display_stats(p1.stats)
    vwt.display_stats(p2.stats)

def main() -> None:
    train(RUNS)

if __name__ == "__main__":
    main()