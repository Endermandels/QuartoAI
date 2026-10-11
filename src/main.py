from global_defs.stats import Stats, QLearnStats
from controller import Controller
from view import View, TerminalView, BColors
from model import Model
from agent import *
from time import perf_counter
from datetime import datetime
import cProfile, pstats

RUNS: int = 1000

def run(vw: View
        , vwt: TerminalView
        , a1: Agent
        , a2: Agent
        , ngames: int
        , headless: bool = True) -> None:
    start_time: float
    end_time: float
    
    start_time = perf_counter()
    mdl = Model(keep_logs=not headless)
    ctrl = Controller(mdl, vw if headless else vwt, a1, a2, ngames)
    ctrl.run()
    end_time = perf_counter()
    print(f"Runtime: {(end_time - start_time):.6f} seconds")
    
    vwt.display_stats(a1.stats)
    vwt.display_stats(a2.stats)
    
def _get_agent_from_input(self, inp: str, is_p1: bool) -> Agent | None:
    def is_float(f) -> bool:
        try:
            float(f)
        except:
            return None
        return True
    
    agent: Agent = None
    
    if inp == "h":
        agent = HumanAgent(is_p1, Stats("Human"), self)
    elif inp == "r":
        agent = RandomAgent(is_p1, Stats("Random"))
    elif inp == "h":
        agent = HeuristicAgent(is_p1, Stats("Heuristic"))
    elif inp == "q":
        # Ask for more detail
        epsilon: float = 1.0
        alpha: float = 0.1
        gamma: float = 1.0
        
        self._print("? Input: '[e=1.0],[a=0.1],[y=1.0],[e_decay=0.7]'", BColors.CYAN)
        inp = input("> ").strip().lower()
        
        if len(inp) > 0 and is_float(inp[0]):
            epsilon = float(inp[0])
        if len(inp) > 1 and is_float(inp[1]):
            alpha = float(inp[1])
        if len(inp) > 2 and is_float(inp[2]):
            gamma = float(inp[2])
        
        agent = QLearnAgent(is_p1, QLearnStats("QLearn"), epsilon, alpha, gamma)
    
    return agent

def main() -> None:
    vw: View = View()
    vwt: View = TerminalView()
    running: bool = True
    rnd1: Agent = RandomAgent(Stats("Random1"))
    rnd2: Agent = RandomAgent(Stats("Random2"))
    hmn1: Agent = HumanAgent(Stats("Human1"), vwt)
    hmn2: Agent = HumanAgent(Stats("Human2"), vwt)
    hrs1: Agent = HeuristicAgent(Stats("Heuristic1"))
    hrs2: Agent = HeuristicAgent(Stats("Heuristic2"))
    qlr1: Agent = QLearnAgent(QLearnStats("QLearn1"))
    qlr2: Agent = QLearnAgent(QLearnStats("QLearn2"))
    a1Map: dict[str, Agent] = {
        "rnd": rnd1,
        "hmn": hmn1,
        "hrs": hrs1,
        "qlr": qlr1,
    }
    a2Map: dict[str, Agent] = {
        "rnd": rnd2,
        "hmn": hmn2,
        "hrs": hrs2,
        "qlr": qlr2,
    }
    a1: Agent = rnd1
    a2: Agent = rnd2
    ngames: int = RUNS
    headless: bool = True
    inp: str
    
    # Set agents
    # Set runs
    # Set hyperparameters
    # Set headless mode
    # Set q table save file
    # Set q table load file
    # Run games
    # Interrupt games
            
    while running:
        print(f"? Input:")
        inp: str = input("> ").strip().lower()
        
        # Commands
        if inp == "q":
            running = False
        elif inp == "r":
            run(vw, vwt, a1, a2, ngames, headless)
        # TODO: Add profiling in, maybe?
        # elif inp == "prf":
        #     cProfile.run(f"run({vw}, {vwt}, {a1}, {a2}, {ngames}, {headless})", "prof.out")
        #     pstats.Stats("prof.out").sort_stats("tottime").print_stats(10)
        
        # Agents
        elif inp.startswith("a1=") and inp[3:] in a1Map:
            a1 = a1Map[inp[3:]]
            print(a1.stats)
        elif inp.startswith("a2=") and inp[3:] in a2Map:
            a2 = a2Map[inp[3:]]
            print(a2.stats)
        elif inp == "ca1":
            a1.clear_stats()
            print(a1.stats)
        elif inp == "ca2":
            a2.clear_stats()
            print(a2.stats)
        elif inp == "pa1":
            print(a1.stats)
        elif inp == "pa2":
            print(a2.stats)
        
        # Hyperparameters
        elif inp == "hdls":
            headless = not headless
            print(f">>> Headles: {headless}")
        elif inp == "phdls":
            print(f">>> Headles: {headless}")
        elif inp == "png":
            print(f">>> Games: {ngames}")
        
        # Unknown
        else:
            print(f"! Unknown: {inp}")
        

if __name__ == "__main__":
    main()