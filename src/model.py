from __future__ import annotations
from global_defs.state import (
    PiecePlace, PieceGive, Action, State, Winner, 
    WHITE_PIECES, BLACK_PIECES, ALL_EMPTY, GRID_LEN, PIECE_SIZE, PIECE_MASK
)
from enum import StrEnum

class Errors(StrEnum):
    NO_PIECE_TO_GIVE = "No piece to give"
    BOARD_SPACE_OCCUPIED = "Board space occupied"
    COORDINATES_OUT_OF_BOUNDS = "Coordinates are out of bounds"
    
class Model:
    def __init__(self, start_state: State = None):
        self.state: State = start_state
        self.error_log: list[Errors] = []
        self.move_log: list[str] = []
        self.winner: Winner = Winner.NONE
        
        # Default State
        if self.state == None:
            self.state = State(
                0,
                ALL_EMPTY,
                WHITE_PIECES | BLACK_PIECES,
                PieceGive.EMPTY.value,
            )
    
    def is_p1_turn(self, state: State) -> bool:
        """ Returns whether the current action should be done by P1 (true) or P2 (false) """
        res: bool = False
        
        if state.given_piece == PieceGive.EMPTY:
            # If p1 pieces left == p2 pieces left and no piece has been given, it is p1's turn to give
            if state.remaining_pieces.bit_count() % 2 == 0:
                res = True
            # If p1 pieces left != p2 pieces left and no piece has been given, it is p2's turn to give
             
        # If a black piece has been given, it is p1's turn to place 
        elif (state.given_piece & BLACK_PIECES) != 0:
            res = True
            
        # If a white piece has been given, it is p2's turn to place
        
        return res
    
    def is_legal_give_piece(self, state: State, action: Action) -> bool:
        is_legal: bool = False
        pieces: int = state.remaining_pieces
        
        if action == None:
            return is_legal
        
        # Check that current player has the desired piece available to give
        pieces = (pieces & WHITE_PIECES) if self.is_p1_turn(state) else (pieces & BLACK_PIECES)
        if (action.piece & pieces) == action.piece:
            is_legal = True
        else:
            self.error_log.append(Errors.NO_PIECE_TO_GIVE)
        
        return is_legal
    
    def is_legal_place_piece(self, state: State, action: Action) -> bool:
        is_legal: bool = False
        
        if action == None:
            return is_legal
        
        # Check that the specified coordinates are within the board
        if 0 <= action.space and action.space < GRID_LEN * GRID_LEN:
            is_legal = True
            
            # Check that the board space specified is EMPTY
            if ((state.empty >> action.space) & 1) != 1:
                is_legal = False
                self.error_log.append(Errors.BOARD_SPACE_OCCUPIED)
        else:
            self.error_log.append(Errors.COORDINATES_OUT_OF_BOUNDS)
        
        return is_legal
    
    def legal_give_actions(self, state: State) -> list[int]:
        """ Return a list of legal pieces to give """
        actions: list[int] = []
        pieces: int = WHITE_PIECES if self.is_p1_turn(state) else BLACK_PIECES
        shift: int = 0 if pieces == WHITE_PIECES else 8
        
        for i in range(pieces.bit_length()):
            piece: int = (1 << i) << shift
            if (state.remaining_pieces & piece) == piece:
                actions.append(piece)
                
        return actions

    def legal_place_actions(self, state: State) -> list[int]:
        """ Return a list of empty spaces on the board """
        actions: list[int] = []
        
        for i in range(GRID_LEN * GRID_LEN):
            if ((state.empty >> i) & 1) == 1:
                actions.append(i)
            
        return actions
    
    def give_piece(self, state: State, action: Action, update_state: bool = True) -> State:
        """ Give the specified piece to the opposite player """
        new_remaining_pieces: int = state.remaining_pieces
        given_piece: int = PieceGive.EMPTY
        new_state: State
        
        if not self.is_legal_give_piece(state, action):
            return state
        
        new_remaining_pieces = state.remaining_pieces & (~action.piece)
        given_piece = action.piece
        new_state = State(
            state.board,
            state.empty,
            new_remaining_pieces,
            given_piece,
        )
        
        if update_state:
            self.move_log.append(f"{"P1 gave P2" if self.is_p1_turn(self.state) else "P2 gave P1"} a {PieceGive(given_piece).name}")
            self.state = new_state
        
        return new_state
    
    def place_piece(self, state: State, action: Action, update_state: bool = True) -> State:
        """ Opposite player places the given piece """
        piece_place: int
        new_state: State
        
        if not self.is_legal_place_piece(state, action):
            return state
        
        piece_place = PiecePlace[PieceGive(state.given_piece).name].value
        
        new_state = State(
            state.board | (piece_place << (action.space * PIECE_SIZE)),
            state.empty & (~(1 << action.space)), # Clear empty space
            state.remaining_pieces,
            PieceGive.EMPTY.value, # Reset given_piece
        )
        
        if update_state:
            self.move_log.append(f"{"P1" if self.is_p1_turn(self.state) else "P2"} " \
                                f"placed {PieceGive(self.state.given_piece).name} at " \
                                f"({int(action.space / GRID_LEN)}, {action.space % GRID_LEN})")
            self.winner = self.check_winner(self.state, action.space, piece_place)
            self.state = new_state
        
        return new_state
    
    def check_winner(self, state: State, space: int, piece: int) -> Winner:
        """ Check if placing given piece at given space results in a win """
        winner: Winner = Winner.NONE
        
        if (state.empty & (1 << space)) != 0:
            r: int = int(space / GRID_LEN)
            c: int = space % GRID_LEN
            AND: tuple[int, ...] = [piece, piece, piece, piece]
            OR: tuple[int, ...] = [piece, piece, piece, piece]
            is_diagonal_same: bool = (r == c)
            is_diagonal_diff: bool = (GRID_LEN - 1 - r == c)
            
            # Check win for this position's row, col (and potentially diagonal)
            for i in range(GRID_LEN):
                shift: int
                board_piece: int 
                empty_penalty: int
                if i != c:
                    shift = ((GRID_LEN * r) + i)
                    board_piece = ((state.board >> (shift * PIECE_SIZE)) & PIECE_MASK)
                    empty_penalty = 0xF if (state.empty & (1 << shift)) != 0 else 0x0
                    AND[0] &= board_piece
                    OR[0] |= board_piece | empty_penalty # if empty space, board_piece will be 0, which is a valid piece
                if i != r:
                    shift = ((GRID_LEN * i) + c)
                    board_piece = ((state.board >> (shift * PIECE_SIZE)) & PIECE_MASK)
                    empty_penalty = 0xF if (state.empty & (1 << shift)) != 0 else 0x0
                    AND[1] &= board_piece
                    OR[1] |= board_piece | empty_penalty
                
                    if is_diagonal_same:
                        shift = ((GRID_LEN * i) + i)
                        board_piece = ((state.board >> (shift * PIECE_SIZE)) & PIECE_MASK)
                        empty_penalty = 0xF if (state.empty & (1 << shift)) != 0 else 0x0
                        AND[2] &= board_piece
                        OR[2] |= board_piece | empty_penalty
                    elif is_diagonal_diff:
                        shift = ((GRID_LEN * i) + (GRID_LEN - 1 - i))
                        board_piece = ((state.board >> (shift * PIECE_SIZE)) & PIECE_MASK)
                        empty_penalty = 0xF if (state.empty & (1 << shift)) != 0 else 0x0
                        AND[3] &= board_piece
                        OR[3] |= board_piece | empty_penalty
            
            # Each piece is a bitmask of categories
            # For pieces AND'd together, if they retain a one, that means that category is present in all 4 spots
            # For pieces OR'd together, if they retain a zero, and they do not have any empty spaces, 
            #   that means that category is present in all 4 spots
            if (
                (AND[0] != 0 or OR[0].bit_count() < 4)
                or (AND[1] != 0 or OR[1].bit_count() < 4)
                or (is_diagonal_same and (AND[2] != 0 or OR[2].bit_count() < 4))
                or (is_diagonal_diff and (AND[3] != 0 or OR[3].bit_count() < 4))
            ):
                winner = Winner.PLAYER_1 if (PieceGive[PiecePlace(piece).name] & WHITE_PIECES) == 0 else Winner.PLAYER_2
            elif state.remaining_pieces == 0:
                winner = Winner.TIE
            
        return winner
    
    def final_reward(self, is_p1: bool) -> float:
        rew: float = 0.0
        
        if self.winner == Winner.NONE:
            rew = 0.0
        elif (self.winner == Winner.PLAYER_1 and is_p1) or (self.winner == Winner.PLAYER_2 and not is_p1):
            rew = 1.0
        elif self.winner != Winner.TIE:
            -1.0
        
        return rew