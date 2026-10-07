from __future__ import annotations
from global_defs.state import Action, PiecePlace, PieceGive, Winner
from global_defs.stats import Stats
from model import Model

class BColors:
    """ Text colors """
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

WARN_COL = BColors.YELLOW
ERROR_COL = BColors.RED

class View:
    def __init__(self):
        self.quit_input: bool = False # Input to quit the game
    
    def query_give_piece(self, mdl: Model) -> Action | None:
        """ Returns the piece to give to the other player, or None on a different input (i.e. quit) """
        return None
    
    def query_place_piece(self, mdl: Model) -> Action | None:
        """ Returns the coords to place the given piece, or None on a different input (i.e. quit) """
        return None
    
    def display_winner(self, mdl: Model) -> None:
        pass
    
    def display_stats(self, stats: Stats) -> None:
        pass
    
    def update(self, mdl: Model) -> None:
        pass
    
class TerminalView(View):
    def __init__(self):
        super().__init__()
        self._print("$$$ Quarto AI $$$", BColors.GREEN, True)
        
    def query_give_piece(self, mdl: Model) -> Action | None:
        action: Action = None
        inp: str = ""

        self._print(f"? {"P1" if mdl.is_p1_turn(mdl.state) else "P2"} which piece would you like to give", BColors.CYAN)        
        inp = input("> ").strip().lower()
        
        if inp in ["q", "quit"]:
            self.quit_input = True
        elif inp in ["p", "print"]:
            self._print_board(mdl.state.board)
        elif len(inp) == 3:
            piece_name: str = ""
            valid_piece: bool = True
            
            piece_name += "WHITE_" if mdl.is_p1_turn(mdl.state) else "BLACK_"

            if inp[0] == "s":
                piece_name += "SHORT_"
            elif inp[0] == "t":
                piece_name += "TALL_"
            else:
                self._warn(f"! Unknown tall/short input: {inp[0]}")
                valid_piece = False
            
            if inp[1] == "s":
                piece_name += "SQUARE_"
            elif inp[1] == "c":
                piece_name += "CIRCLE_"
            else:
                self._warn(f"! Unknown square/circle input: {inp[0]}")
                valid_piece = False
            
            if inp[2] == "h":
                piece_name += "HOLE"
            elif inp[2] == "s":
                piece_name += "SOLID"
            else:
                self._warn(f"! Unknown hole/solid input: {inp[0]}")
                valid_piece = False
            
            if valid_piece:  
                action = Action(piece=PieceGive[piece_name].value)
        else:
            self._warn(f"! Unknown input: {inp}")
            
        return action
        
    def query_place_piece(self, mdl: Model) -> Action | None:
        action: Action = None
        inp: str = ""
        inp_split: list[str] = []

        self._print( f"? {"P1" if mdl.is_p1_turn(mdl.state) else "P2"} " \
                    f"where would you like to place the {PieceGive(mdl.state.given_piece).name}", BColors.CYAN)
        inp = input("> ").strip().lower()
        inp_split = inp.split(",")
        
        if inp in ["q", "quit"]:
            self.quit_input = True
        elif inp in ["p", "print"]:
            self._print_board(mdl.state.board)
        elif len(inp_split) == 2 and all([s.isdigit() for s in inp_split]):
            action = Action(board_coords=(int(inp_split[0]), int(inp_split[1])))
        else:
            self._warn(f"! Unknown input: {inp}")
        
        return action
    
    def display_winner(self, mdl: Model) -> None:
        if mdl.winner == Winner.TIE:
            self._print(f"* Tie!", BColors.YELLOW, True)
        else:
            self._print(f"* {mdl.winner.name} Won!", BColors.GREEN, True)
        self._print_board(mdl.state.board)

    def display_stats(self, stats: Stats) -> None:
        self._print("-----------------------------------------------------")
        self._print(f">>> Agent: \t\t{stats.agent_name}")
        self._print(f">>> Games Won: \t\t{stats.games_won}")
        self._print(f">>> Games Lost: \t{stats.games_lost}")
        self._print(f">>> Games Tied: \t{stats.games_tied}")
        self._print(f">>> Games Played: \t{stats.games_played}")
    
    def update(self, mdl: Model) -> None:
        while len(mdl.error_log) > 0:
            self._warn(f"! Error: {mdl.error_log.pop(0)}")
        while len(mdl.move_log) > 0:
            self._print(f"* {mdl.move_log.pop(0)}")
    
    def _print(self, string: str, col: BColors = BColors.ENDC, bold: bool = False) -> None:
        """ Print string with specified color """
        print(f"{BColors.BOLD if bold else ""}{col}{string}{BColors.ENDC}")

    def _warn(self, string: str) -> None:
        """ Print a warning string """
        print(f"{BColors.BOLD}{WARN_COL}{string}{BColors.ENDC}")
        
    def _error(self, string: str) -> None:
        """ Print an error string """
        print(f"{BColors.BOLD}{ERROR_COL}{string}{BColors.ENDC}")
        
    def _print_board(self, board: tuple[tuple[int, ...], ...]) -> None:
        """ Prints the given board """
        for row in board:
            print("| ", end="")
            for piece in row:
                # Represent each piece by the first letter of each category (i.e. BTSH for BLACK_TALL_SQUARE_HOLE)
                piece_repr: str = "".join([s[0] for s in PiecePlace(piece).name.split("_")])
                print(f"{piece_repr}\t| ", end="")
            print()