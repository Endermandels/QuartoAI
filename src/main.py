from global_defs.stats import Stats
from controller import Controller
from view import View, TerminalView
from model import Model
from agent import HeuristicAgent, RandomAgent, HumanAgent, QLearnAgent, Agent
from time import perf_counter
import pickle
from datetime import datetime
import cProfile, pstats

RUNS: int = 1000

def train(runs) -> None:
    vw: View = View()
    vwt: View = TerminalView()
    p1: Agent = RandomAgent(True, Stats("Random1"))
    # p2: Agent = HumanAgent(False, Stats("Human2"), vwt)
    # p2: Agent = RandomAgent(False, Stats("Random2"))
    p2: Agent = HeuristicAgent(False, Stats("Heuristic2"))
    # p2: Agent = QLearnAgent(False, Stats("Q-Learn2"), 1.0, 0.1, 1.0, 1 / (runs * 0.7))
    end_time: float
    start_time: float
    
    # # Load agent
    # with open(f"../agents/{p2.stats.agent_name}_0.05_0.10_1.00_1000000", "rb") as file:
    #     save: QLearnAgent = pickle.load(file)
    #     p2.q_table = save.q_table
    
    start_time = perf_counter()
    
    for i in range(runs):
        mdl = Model()
        ctrl = Controller(mdl, vw, p1, p2)
        ctrl.run()
        # print(f"Game {i + 1} Completed")
    
    end_time = perf_counter()
    print(f"Runtime: {(end_time - start_time):.6f} seconds")
    # print(p2.hit_rate / p2.lookups)
    
    vwt.display_stats(p1.stats)
    vwt.display_stats(p2.stats)
    
    # # Save agent
    # with open(f"../agents/{p2.stats.agent_name}_{p2.epsilon:.2f}_{p2.alpha:.2f}_{p2.gamma:.2f}_{runs}", "wb") as file:
    #     pickle.dump(p2, file)

def main() -> None:
    cProfile.run(f"train({RUNS})", "prof.out")
    pstats.Stats("prof.out").sort_stats("tottime").print_stats(10)
    # train(RUNS)

if __name__ == "__main__":
    main()