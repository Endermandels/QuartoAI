from __future__ import annotations
from global_defs.state import *
from enum import StrEnum

class Errors(StrEnum):
    NO_PIECE_TO_GIVE = "No piece to give"
    GIVE_PIECE_EXISTS = "A piece has already been given"
    BOARD_SPACE_OCCUPIED = "Board space occupied"
    COORDINATES_OUT_OF_BOUNDS = "Coordinates are out of bounds"
    
class Model:
    def __init__(self, start_state: tuple[int, ...] = None, keep_logs: bool = False):
        self.state: tuple[int, ...] = start_state
        self.keep_logs = keep_logs
        self.error_log: list[Errors] = []
        self.move_log: list[str] = []
        self.winner: Winner = Winner.NONE
        self.LINES: dict[int, list[tuple[int, ...]]] = self._compute_lines()
                
        # Default State
        if self.state == None:
            self.state = (
                STATE_BOARD_DEFAULT,
                STATE_EMPTY_DEFAULT,
                STATE_REMAINING_DEFAULT,
                STATE_GIVEN_DEFAULT,
            )
    
    def is_give_phase(self, state: tuple[int, ...]) -> bool:
        """ Returns whether the current phase is the give phase (true) or the place phase (false) """
        return (state[STATE_GIVEN_IDX] & STATE_GIVEN__PIECE_MASK) == EMPTY_PIECE
    
    def is_p1_turn(self, state: tuple[int, ...]) -> bool:
        """ Returns whether the current action should be done by P1 (true) or P2 (false) """
        return (state[STATE_GIVEN_IDX] & STATE_GIVEN__IS_P1_TURN_MASK) == STATE_GIVEN__IS_P1_TURN_MASK
    
    def is_legal_give_piece(self, state: tuple[int, ...], action: tuple[int, ...] | None) -> bool:
        is_legal: bool = False
        
        if action == None:
            return is_legal
    
        # Check that current player has the desired piece available to give
        if ((state[STATE_REMAINING_IDX] >> action[ACTION_PIECE_IDX]) & 1) == 1:
            is_legal = True
        
            # Check that there is no current given piece
            if (state[STATE_GIVEN_IDX] & STATE_GIVEN__PIECE_MASK) != EMPTY_PIECE:
                is_legal = False
                if self.keep_logs:
                    self.error_log.append(Errors.GIVE_PIECE_EXISTS)
        elif self.keep_logs:
            self.error_log.append(Errors.NO_PIECE_TO_GIVE)
        
        return is_legal
    
    def is_legal_place_piece(self, state: tuple[int, ...], action: tuple[int, ...]) -> bool:
        is_legal: bool = False
        
        if action == None:
            return is_legal
        
        # Check that the specified coordinates are within the board
        if 0 <= action[ACTION_SPACE_IDX] and action[ACTION_SPACE_IDX] < GRID_LEN * GRID_LEN:
            is_legal = True
            
            # Check that the board space specified is EMPTY
            if ((state[STATE_EMPTY_IDX] >> action[ACTION_SPACE_IDX]) & 1) != 1:
                is_legal = False
                if self.keep_logs:
                    self.error_log.append(Errors.BOARD_SPACE_OCCUPIED)
        elif self.keep_logs:
            self.error_log.append(Errors.COORDINATES_OUT_OF_BOUNDS)
        
        return is_legal
    
    def legal_give_actions(self, state: tuple[int, ...]) -> list[int]:
        """ Return a list of legal pieces to give """
        actions: list[int] = []
        shift: int = 0 if self.is_p1_turn(state) else WHITE_PIECES_SIZE
        
        for i in range(WHITE_PIECES_SIZE):
            piece: int = i + shift
            if (state[STATE_REMAINING_IDX] & (1 << piece)) != 0:
                actions.append(piece)
                
        return actions

    def legal_place_actions(self, state: tuple[int, ...]) -> list[int]:
        """ Return a list of empty spaces on the board """
        actions: list[int] = []
        
        for i in range(GRID_LEN * GRID_LEN):
            if ((state[STATE_EMPTY_IDX] >> i) & 1) == 1:
                actions.append(i)
            
        return actions
    
    def give_piece(self, state: tuple[int, ...], action: tuple[int, ...], update_state: bool = True) -> tuple[int, ...]:
        """ Give the specified piece to the opposite player """
        new_state: tuple[int, ...]
        new_turn_mask: int = (state[STATE_GIVEN_IDX] & STATE_GIVEN__IS_P1_TURN_MASK) ^ STATE_GIVEN__IS_P1_TURN_MASK
        
        if not self.is_legal_give_piece(state, action):
            return state
        
        new_state = (
            state[STATE_BOARD_IDX],
            state[STATE_EMPTY_IDX],
            state[STATE_REMAINING_IDX] & (~(1 << action[ACTION_PIECE_IDX])),
            action[ACTION_PIECE_IDX] | new_turn_mask, # Switch turns
        )
        
        if update_state:
            if self.keep_logs:
                self.move_log.append(f"{"P1 gave P2" if self.is_p1_turn(self.state) else "P2 gave P1"}" \
                                     f" a {Piece(action[ACTION_PIECE_IDX]).name}")
            self.state = new_state
        
        return new_state
    
    def place_piece(self, state: tuple[int, ...], action: tuple[int, ...], update_state: bool = True) -> tuple[int, ...]:
        """ Opposite player places the given piece """
        new_state: tuple[int, ...]
        
        if not self.is_legal_place_piece(state, action):
            return state
        
        new_state = (
            state[STATE_BOARD_IDX] | ((state[STATE_GIVEN_IDX] & STATE_GIVEN__PIECE_MASK) << (action[ACTION_SPACE_IDX] * PIECE_SIZE)),
            state[STATE_EMPTY_IDX] & (~(1 << action[ACTION_SPACE_IDX])), # Clear empty space
            state[STATE_REMAINING_IDX],
            (state[STATE_GIVEN_IDX] & STATE_GIVEN__IS_P1_TURN_MASK) | EMPTY_PIECE, # Reset given_piece
        )
        
        if update_state:
            if self.keep_logs:
                self.move_log.append(f"{"P1" if self.is_p1_turn(self.state) else "P2"} " \
                                    f"placed {Piece(self.state[STATE_GIVEN_IDX] & STATE_GIVEN__PIECE_MASK).name} at " \
                                    f"({int(action[ACTION_SPACE_IDX] / GRID_LEN)}, {action[ACTION_SPACE_IDX] % GRID_LEN})")
                
            if self.check_winner_fast(new_state[STATE_BOARD_IDX], new_state[STATE_EMPTY_IDX], action[ACTION_SPACE_IDX]):
                self.winner = Winner.PLAYER_1 if self.is_p1_turn(self.state) else Winner.PLAYER_2
            elif new_state[STATE_EMPTY_IDX] == 0:
                self.winner = Winner.TIE
            
            self.state = new_state
        
        return new_state
    
    def check_winner_fast(self, board: int, empty: int, space: int) -> bool:
        """ Check if the given space shows in a win """
        is_win: bool = False
        
        for empty_mask, s0, s1, s2, s3 in self.LINES[space]:
            if empty & empty_mask != 0:
                continue # there is an empty space in this sequence, so no win is possible
            a: int = (board >> (s0 * PIECE_SIZE)) & PIECE_MASK
            b: int = (board >> (s1 * PIECE_SIZE)) & PIECE_MASK
            c: int = (board >> (s2 * PIECE_SIZE)) & PIECE_MASK
            d: int = (board >> (s3 * PIECE_SIZE)) & PIECE_MASK
            if (a & b & c & d) != 0 or ((~(a | b | c | d) & PIECE_MASK) != 0):
                is_win = True
                break
        
        return is_win
        
    def final_reward(self, is_p1: bool) -> float:
        rew: float = 0.0
        
        if self.winner == Winner.NONE:
            rew = 0.0
        elif (self.winner == Winner.PLAYER_1 and is_p1) or (self.winner == Winner.PLAYER_2 and not is_p1):
            rew = 1.0
        elif self.winner != Winner.TIE:
            -1.0
        
        return rew
    
    def reset(self) -> None:
        self.state = (
            STATE_BOARD_DEFAULT,
            STATE_EMPTY_DEFAULT,
            STATE_REMAINING_DEFAULT,
            STATE_GIVEN_DEFAULT,
        )
        self.winner: Winner = Winner.NONE
    
    def _compute_lines(self) -> dict[int, list[tuple[int, ...]]]:
        lines: dict[int, list[tuple[int, ...]]] = {} # empty mask, shift 0, shift 1, shift 2, shift 3
        
        for space in range(GRID_LEN * GRID_LEN):
            r: int = int(space / GRID_LEN)
            c: int = space % GRID_LEN
            
            # Row and column
            lines[space] = [
                (PIECE_MASK << (r * GRID_LEN), r * GRID_LEN, r * GRID_LEN + 1, r * GRID_LEN + 2, r * GRID_LEN + 3), # row
                (1 << c | 1 << c << (GRID_LEN) | 1 << c << (2 * GRID_LEN) | 1 << c << (3 * GRID_LEN),
                 c, c + GRID_LEN, c + 2 * GRID_LEN, c + 3 * GRID_LEN) # col
            ]
            
            # Same diagonal
            if r == c:
                lines[space].append([0x8421, 0, GRID_LEN + 1, GRID_LEN * 2 + 2, GRID_LEN * 3 + 3])
            # Opposite diagonal
            if GRID_LEN - 1 - r == c:
                lines[space].append([0x1248, GRID_LEN - 1, GRID_LEN * 2 - 2, GRID_LEN * 3 - 3, GRID_LEN * 4 - 4])
    
        return lines