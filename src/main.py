from global_defs.stats import Stats, QLearnStats
from controller import Controller
from view import View, TerminalView
from model import Model
from agent import *
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
    # p2: Agent = QLearnAgent(False, QLearnStats("Q-Learn2"), 1.0, 0.1, 1.0, 1 / (runs * 0.7))
    end_time: float
    start_time: float
    
    # # Load agent
    # start_time = perf_counter()
    # with open(f"agents/{p2.stats.agent_name}_0.05_0.10_1.00_100000", "rb") as file:
    #     p2.q_table = pickle.load(file)
    # end_time = perf_counter()
    # print(f"Load time: {(end_time - start_time):.6f} seconds")
    
    start_time = perf_counter()
    
    mdl = Model(keep_logs=False)
    ctrl = Controller(mdl, vw, p1, p2, runs)
    ctrl.run()
    
    end_time = perf_counter()
    print(f"Runtime: {(end_time - start_time):.6f} seconds")
    
    vwt.display_stats(p1.stats)
    vwt.display_stats(p2.stats)
    
    # # Save agent
    # start_time = perf_counter()
    # with open(f"agents/{p2.stats.agent_name}_{p2.epsilon:.2f}_{p2.alpha:.2f}_{p2.gamma:.2f}_{runs}", "wb") as file:
    #     pickle.dump(p2.q_table, file)
    # end_time = perf_counter()
    # print(f"Save time: {(end_time - start_time):.6f} seconds")

def main() -> None:
    # cProfile.run(f"train({RUNS})", "prof.out")
    # pstats.Stats("prof.out").sort_stats("tottime").print_stats(10)
    train(RUNS)

if __name__ == "__main__":
    main()