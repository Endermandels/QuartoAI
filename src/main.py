from controller import Controller
from view import TerminalView
from model import Model
from agent import HumanAgent, RandomAgent

def main() -> None:
    mdl = Model()
    vw = TerminalView()
    p1 = RandomAgent(True)
    p2 = RandomAgent(False)
    ctrl = Controller(mdl, vw, p1, p2)
    ctrl.run()

if __name__ == "__main__":
    main()