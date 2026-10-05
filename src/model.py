from __future__ import annotations
from global_defs.state import PieceMask, ActionGive, ActionPlace, State, Winner, WHITE_PIECES, BLACK_PIECES
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
        
        # Default State
        if self.state == None:
            self.state = State(
                (
                    (PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY),
                    (PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY),
                    (PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY),
                    (PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY, PieceMask.EMPTY),
                ),
                WHITE_PIECES | BLACK_PIECES,
                PieceMask.EMPTY,
            )
    
    def is_p1_turn(self, state: State) -> bool:
        """ Returns whether the current action should be done by P1 (true) or P2 (false) """
        res: bool = False
        
        if state.given_piece == PieceMask.EMPTY:
            # If p1 pieces left == p2 pieces left and no piece has been given, it is p1's turn to give
            if state.remaining_pieces.bit_count() % 2 == 0:
                res = True
            # If p1 pieces left != p2 pieces left and no piece has been given, it is p2's turn to give
             
        # If a black piece has been given, it is p1's turn to place 
        elif (state.given_piece & BLACK_PIECES) != 0:
            res = True
            
        # If a white piece has been given, it is p2's turn to place
        
        return res
    
    def is_legal_give_piece(self, action: ActionGive) -> bool:
        is_legal: bool = False
        pieces: int = self.state.remaining_pieces
        
        if action == None:
            return is_legal
        
        # Check that current player has the desired piece available to give
        pieces = (pieces & WHITE_PIECES) if self.is_p1_turn(self.state) else (pieces & BLACK_PIECES)
        if (action.piece & pieces) == action.piece:
            is_legal = True
        else:
            self.error_log.append(Errors.NO_PIECE_TO_GIVE)
        
        return is_legal
    
    def is_legal_place_piece(self, action: ActionPlace) -> bool:
        is_legal: bool = False
        
        if action == None:
            return is_legal
        
        # Check that the specified coordinates are within the board
        if (
            0 <= action.row and action.row < len(self.state.board)
            and 0 <= action.col and action.col < len(self.state.board[0])
        ):
            is_legal = True
            
            # Check that the board space specified is EMPTY
            if self.state.board[action.row][action.col] != PieceMask.EMPTY:
                is_legal = False
                self.error_log.append(Errors.BOARD_SPACE_OCCUPIED)
        else:
            self.error_log.append(Errors.COORDINATES_OUT_OF_BOUNDS)
        
        return is_legal
    
    def give_piece(self, action: ActionGive) -> State:
        """ Give the specified piece to the opposite player """
        new_remaining_pieces: int = self.state.remaining_pieces
        given_piece: int = PieceMask.EMPTY
        
        if not self.is_legal_give_piece(action):
            return self.state
        
        new_remaining_pieces = self.state.remaining_pieces & (~action.piece)
        given_piece = action.piece
        self.move_log.append(f"{"P1 gave P2" if self.is_p1_turn(self.state) else "P2 gave P1"} a {PieceMask(given_piece).name}")
        
        self.state = State(
            self.state.board,
            new_remaining_pieces,
            given_piece,
        )
        
        return self.state
    
    def place_piece(self, action: ActionPlace) -> State:
        """ Opposite player places the given piece """
        new_board: tuple[tuple[int, ...], ...]
        new_row: tuple[int, ...]
        
        if not self.is_legal_place_piece(action):
            return self.state
        
        new_row = (
            self.state.board[action.row][:action.col] 
            + (self.state.given_piece, ) 
            + self.state.board[action.row][action.col + 1:]
        )
        new_board = (
            self.state.board[:action.row] 
            + (new_row, ) 
            + self.state.board[action.row + 1:]
        )
        self.move_log.append(f"{"P1" if self.is_p1_turn(self.state) else "P2"} " \
                             f"placed {PieceMask(self.state.given_piece).name} at ({action.row}, {action.col})")
        
        self.state = State(
            new_board,
            self.state.remaining_pieces,
            PieceMask.EMPTY, # Reset given_piece
        )
        
        return self.state
    
    def check_winner(self, state: State) -> Winner:
        new_winner: Winner = Winner.NONE
        at_least_one_empty: bool = False # Keeps track of whether there is at least one EMPTY space left
        
        for j in range(len(state.board)):
            category_counts: dict = {} # key = category (i.e. "WH" for white), value = count
            
            # Check rows, columns and diagonals
            # Count each category
            # If at least one category has a count of the length of the board, the winner is the opposite player
            for i in range(len(state.board[j])):
                row_categories: list[str] = [s[0:2] for s in PieceMask(state.board[j][i]).name.split("_")]
                col_categories: list[str] = [s[0:2] for s in PieceMask(state.board[i][j]).name.split("_")]
                dia_categories: list[str] = [PieceMask.EMPTY.name[0:2]]
                if j == 0:
                    dia_categories = [s[0:2] for s in PieceMask(state.board[j + i][j + i]).name.split("_")]
                    dia_categories = [s[0:2] for s in PieceMask(state.board[j + i][len(state.board) - 1 - i]).name.split("_")]

                for cat in row_categories:
                    if cat != "EM": # Filter out EMPTY board spaces
                        rcat: str = "R" + cat
                        if rcat in category_counts:
                            category_counts[rcat] += 1
                        else:
                            category_counts[rcat] = 1
                    else:
                        at_least_one_empty = True # This should cover the whole board

                for cat in col_categories:
                    if cat != "EM": # Filter out EMPTY board spaces
                        ccat: str = "C" + cat
                        if ccat in category_counts:
                            category_counts[ccat] += 1
                        else:
                            category_counts[ccat] = 1

                for cat in dia_categories:
                    if cat != "EM": # Filter out EMPTY board spaces
                        dcat: str = "D" + cat
                        if dcat in category_counts:
                            category_counts[dcat] += 1
                        else:
                            category_counts[dcat] = 1
            
            for value in category_counts.values():
                if value == len(state.board):
                    # The last person who placed a piece then goes to give a piece
                    if self.is_p1_turn(state):
                        new_winner = Winner.PLAYER_1
                    else:
                        new_winner = Winner.PLAYER_2
                    break
            
            if new_winner != Winner.NONE:
                break
        
        # If there is no winner and the board is full, game is tied
        if new_winner == Winner.NONE and not at_least_one_empty:
            new_winner = Winner.TIE
        
        return new_winner
