from global_defs.stats import Stats, QLearnStats
from view import View, TerminalView
from controller import Controller
from model import Model
from agent import *
from time import perf_counter
# import cProfile, pstats

RUNS: int = 1000

def run(vw: View
        , vwt: TerminalView
        , a1: Agent
        , a2: Agent
        , ngames: int
        , headless: bool = True) -> None:
    start_time: float
    end_time: float
    
    if type(a1) == QLearnAgent:
        if a1.load_q_table() == False:
            print("! Aborting run")
            return
    if type(a2) == QLearnAgent:
        if a2.load_q_table() == False:
            print("! Aborting run")
            return
    
    start_time = perf_counter()

    mdl = Model(keep_logs=not headless)
    ctrl = Controller(mdl, vw if headless else vwt, a1, a2, ngames)
    try:
        ctrl.run()
    except KeyboardInterrupt:
        print("* Quitting early")
        
    end_time = perf_counter()
    print(f"Runtime: {(end_time - start_time):.6f} seconds")
    
    vwt.display_stats(a1.stats)
    vwt.display_stats(a2.stats)
    
    if type(a1) == QLearnAgent:
        a1.save_q_table()
    if type(a2) == QLearnAgent:
        a2.save_q_table()
    
def is_float(f: str) -> bool:
    try:
        float(f)
    except:
        return None
    return True

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
    
    while running:
        print(f"? Input:")
        inp: str = input("> ").strip().lower()
        
        # Commands
        if inp == "q":
            running = False
        elif inp == "r":
            run(vw, vwt, a1, a2, ngames, headless)
        # TODO: Add profiling, maybe?
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
        
        # Q-Learn Agents
        elif inp.startswith("q1e=") and type(a1) is QLearnAgent and is_float(inp[4:]):
            a1.epsilon = float(inp[4:])
            print(f">>> Epsilon: {a1.epsilon}")
        elif inp.startswith("q1a=") and type(a1) is QLearnAgent and is_float(inp[4:]):
            a1.alpha = float(inp[4:])
            print(f">>> Alpha: {a1.alpha}")
        elif inp.startswith("q1y=") and type(a1) is QLearnAgent and is_float(inp[4:]):
            a1.gamma = float(inp[4:])
            print(f">>> Gamma: {a1.gamma}")
        elif inp.startswith("q1ed=") and type(a1) is QLearnAgent and is_float(inp[5:]):
            a1.epsilon_decay_rate = float(inp[5:])
            print(f">>> Epsilon Decay: {a1.epsilon_decay_rate}")
        elif inp.startswith("q1sv=") and type(a1) is QLearnAgent:
            a1.save_file = inp[5:]
            print(f">>> Save File: '{a1.save_file}'")
        elif inp.startswith("q1ld=") and type(a1) is QLearnAgent:
            a1.load_file = inp[5:]
            print(f">>> Load File: '{a1.load_file}'")
        elif inp == "pq1" and type(a1) is QLearnAgent:
            print(f">>> Epsilon: {a1.epsilon}")
            print(f">>> Alpha: {a1.alpha}")
            print(f">>> Gamma: {a1.gamma}")
            print(f">>> Epsilon Decay: {a1.epsilon_decay_rate}")
            print(f">>> Save File: '{a1.save_file}'")
            print(f">>> Load File: '{a1.load_file}'")
        
        elif inp.startswith("q2e=") and type(a2) is QLearnAgent and is_float(inp[4:]):
            a2.epsilon = float(inp[4:])
            print(f">>> Epsilon: {a2.epsilon}")
        elif inp.startswith("q2a=") and type(a2) is QLearnAgent and is_float(inp[4:]):
            a2.alpha = float(inp[4:])
            print(f">>> Alpha: {a2.alpha}")
        elif inp.startswith("q2y=") and type(a2) is QLearnAgent and is_float(inp[4:]):
            a2.gamma = float(inp[4:])
            print(f">>> Gamma: {a2.gamma}")
        elif inp.startswith("q2ed=") and type(a2) is QLearnAgent and is_float(inp[5:]):
            a2.epsilon_decay_rate = float(inp[5:])
            print(f">>> Epsilon Decay: {a2.epsilon_decay_rate}")
        elif inp.startswith("q2sv=") and type(a2) is QLearnAgent:
            a2.save_file = inp[5:]
            print(f">>> Save File: '{a2.save_file}'")
        elif inp.startswith("q2ld=") and type(a2) is QLearnAgent:
            a2.load_file = inp[5:]
            print(f">>> Load File: '{a2.load_file}'")
        elif inp == "pq2" and type(a2) is QLearnAgent:
            print(f">>> Epsilon: {a2.epsilon}")
            print(f">>> Alpha: {a2.alpha}")
            print(f">>> Gamma: {a2.gamma}")
            print(f">>> Epsilon Decay: {a2.epsilon_decay_rate}")
            print(f">>> Save File: '{a2.save_file}'")
            print(f">>> Load File: '{a2.load_file}'")
        
        # Game Parameters
        elif inp == "hdls":
            headless = not headless
            print(f">>> Headles: {headless}")
        elif inp == "phdls":
            print(f">>> Headles: {headless}")
        elif inp.startswith("ng=") and inp[3:].isdigit():
            ngames = int(inp[3:])
            print(f">>> Games: {ngames}")
        elif inp == "png":
            print(f">>> Games: {ngames}")
        
        # Unknown
        else:
            print(f"! Unknown: {inp}")
        

if __name__ == "__main__":
    main()