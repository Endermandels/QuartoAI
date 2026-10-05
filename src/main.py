from controller import Controller
from view import TerminalView
from model import Model
from agent import Human

def main() -> None:
    mdl = Model()
    vw = TerminalView()
    p1 = Human(vw)
    p2 = Human(vw)
    ctrl = Controller(mdl, vw, p1, p2)
    ctrl.run()

if __name__ == "__main__":
    main()