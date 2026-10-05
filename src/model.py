from __future__ import annotations
from global_defs.state import BoardSpace, PieceMask, ActionGive, ActionPlace, State, Winner, PIECES_FULL
from enum import StrEnum

class Errors(StrEnum):
    NO_PIECE_TO_GIVE = "No piece to give"
    BOARD_SPACE_OCCUPIED = "Board space occupied"
    COORDINATES_OUT_OF_BOUNDS = "Coordinates are out of bounds"
    
class Model:
    def __init__(self, start_state: State = None):
        self.state: State = start_state
        self.error_log: list[Errors] = []
        
        # Default State
        if self.state == None:
            self.state = State(
                (
                    (BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY),
                    (BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY),
                    (BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY),
                    (BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY),
                ),
                PIECES_FULL,
                PIECES_FULL,
                BoardSpace.EMPTY,
                True,
                Winner.NONE
            )
    
    def is_legal_give_piece(self, action: ActionGive) -> bool:
        is_legal: bool = False
        mask: int
        
        if action == None:
            return is_legal
        
        # Check that current player has the desired piece available to give
        mask = self.state.p1_pieces if self.state.is_p1_turn else self.state.p2_pieces
        if (action.piece & mask) == action.piece:
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
            if not self.state.board[action.row][action.col] == BoardSpace.EMPTY:
                is_legal = False
                self.error_log.append(Errors.BOARD_SPACE_OCCUPIED)
        else:
            self.error_log.append(Errors.COORDINATES_OUT_OF_BOUNDS)
        
        return is_legal
    
    def give_piece(self, action: ActionGive) -> State:
        """ Give the specified piece to the opposite player """
        new_p1_pieces: int = self.state.p1_pieces
        new_p2_pieces: int = self.state.p2_pieces
        given_piece: int = BoardSpace.EMPTY
        
        if not self.is_legal_give_piece(action):
            return self.state

        if self.state.is_p1_turn:
            # Remove piece from p1_pieces
            new_p1_pieces = self.state.p1_pieces & (~action.piece)
            
            # Assign correct white piece to given_piece
            if action.piece == PieceMask.SHORT_CIRCLE_HOLE:
                given_piece = BoardSpace.WHITE_SHORT_CIRCLE_HOLE
            elif action.piece == PieceMask.SHORT_CIRCLE_SOLID:
                given_piece = BoardSpace.WHITE_SHORT_CIRCLE_SOLID
            elif action.piece == PieceMask.SHORT_SQUARE_HOLE:
                given_piece = BoardSpace.WHITE_SHORT_SQUARE_HOLE
            elif action.piece == PieceMask.SHORT_SQUARE_SOLID:
                given_piece = BoardSpace.WHITE_SHORT_SQUARE_SOLID
            elif action.piece == PieceMask.TALL_CIRCLE_HOLE:
                given_piece = BoardSpace.WHITE_TALL_CIRCLE_HOLE
            elif action.piece == PieceMask.TALL_CIRCLE_SOLID:
                given_piece = BoardSpace.WHITE_TALL_CIRCLE_SOLID
            elif action.piece == PieceMask.TALL_SQUARE_HOLE:
                given_piece = BoardSpace.WHITE_TALL_SQUARE_HOLE
            elif action.piece == PieceMask.TALL_SQUARE_SOLID:
                given_piece = BoardSpace.WHITE_TALL_SQUARE_SOLID
        else:
            # Remove piece from p2_pieces
            new_p2_pieces = self.state.p2_pieces & (~action.piece)
            
            # Assign correct black piece to given_piece
            if action.piece == PieceMask.SHORT_CIRCLE_HOLE:
                given_piece = BoardSpace.BLACK_SHORT_CIRCLE_HOLE
            elif action.piece == PieceMask.SHORT_CIRCLE_SOLID:
                given_piece = BoardSpace.BLACK_SHORT_CIRCLE_SOLID
            elif action.piece == PieceMask.SHORT_SQUARE_HOLE:
                given_piece = BoardSpace.BLACK_SHORT_SQUARE_HOLE
            elif action.piece == PieceMask.SHORT_SQUARE_SOLID:
                given_piece = BoardSpace.BLACK_SHORT_SQUARE_SOLID
            elif action.piece == PieceMask.TALL_CIRCLE_HOLE:
                given_piece = BoardSpace.BLACK_TALL_CIRCLE_HOLE
            elif action.piece == PieceMask.TALL_CIRCLE_SOLID:
                given_piece = BoardSpace.BLACK_TALL_CIRCLE_SOLID
            elif action.piece == PieceMask.TALL_SQUARE_HOLE:
                given_piece = BoardSpace.BLACK_TALL_SQUARE_HOLE
            elif action.piece == PieceMask.TALL_SQUARE_SOLID:
                given_piece = BoardSpace.BLACK_TALL_SQUARE_SOLID
        
        self.state = State(
            self.state.board,
            new_p1_pieces,
            new_p2_pieces,
            given_piece,
            self.state.is_p1_turn,
            self.state.winner
        )
        
        return self.state
    
    def place_piece(self, action: ActionPlace) -> State:
        """ Opposite player places the given piece """
        new_board: tuple[tuple[int, ...], ...]
        new_row: tuple[int, ...]
        new_winner: Winner
        
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
        
        # Check for winner/tie (important to call before changing self.state.is_p1_turn)
        new_winner = self._check_winner(new_board)
        
        self.state = State(
            new_board,
            self.state.p1_pieces,
            self.state.p2_pieces,
            BoardSpace.EMPTY, # Reset given_piece
            not self.state.is_p1_turn, # Switch turns
            new_winner
        )
        
        return self.state
    
    def _check_winner(self, board: tuple[tuple[int, ...], ...]) -> Winner:
        new_winner: Winner = Winner.NONE
        at_least_one_empty: bool = False # Keeps track of whether there is at least one EMPTY space left
        
        for j in range(len(board)):
            category_counts: dict = {} # key = category (i.e. "WH" for white), value = count
            
            # Check rows, columns and diagonals
            # Count each category
            # If at least one category has a count of the length of the board, the winner is the opposite player
            for i in range(len(board[j])):
                row_categories: list[str] = [s[0:2] for s in BoardSpace(board[j][i]).name.split("_")]
                col_categories: list[str] = [s[0:2] for s in BoardSpace(board[i][j]).name.split("_")]
                dia_categories: list[str] = [BoardSpace.EMPTY.name[0:2]]
                if j == 0:
                    dia_categories = [s[0:2] for s in BoardSpace(board[j + i][j + i]).name.split("_")]
                    dia_categories = [s[0:2] for s in BoardSpace(board[j + i][len(board) - 1 - i]).name.split("_")]

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
                if value == len(board):
                    if self.state.is_p1_turn:
                        new_winner = Winner.PLAYER_2
                    else:
                        new_winner = Winner.PLAYER_1
                    break
            
            if new_winner != Winner.NONE:
                break
        
        # If there is no winner and the board is full, game is tied
        if new_winner == Winner.NONE and not at_least_one_empty:
            new_winner = Winner.TIE
        
        return new_winner