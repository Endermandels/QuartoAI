from enum import IntEnum
from typing import NamedTuple

class PieceMask(IntEnum):
    """ Mask for piece """
    EMPTY = 0x0000
    WHITE_TALL_SQUARE_HOLE = 0x0001
    WHITE_TALL_SQUARE_SOLID = 0x0002
    WHITE_TALL_CIRCLE_HOLE = 0x0004
    WHITE_TALL_CIRCLE_SOLID = 0x0008
    WHITE_SHORT_SQUARE_HOLE = 0x0010
    WHITE_SHORT_SQUARE_SOLID = 0x0020
    WHITE_SHORT_CIRCLE_HOLE = 0x0040
    WHITE_SHORT_CIRCLE_SOLID = 0x0080
    BLACK_TALL_SQUARE_HOLE = 0x0100
    BLACK_TALL_SQUARE_SOLID = 0x0200
    BLACK_TALL_CIRCLE_HOLE = 0x0400
    BLACK_TALL_CIRCLE_SOLID = 0x0800
    BLACK_SHORT_SQUARE_HOLE = 0x1000
    BLACK_SHORT_SQUARE_SOLID = 0x2000
    BLACK_SHORT_CIRCLE_HOLE = 0x4000
    BLACK_SHORT_CIRCLE_SOLID = 0x8000

WHITE_PIECES: int = (
    PieceMask.WHITE_TALL_CIRCLE_HOLE 
    | PieceMask.WHITE_SHORT_CIRCLE_HOLE
    | PieceMask.WHITE_SHORT_CIRCLE_SOLID
    | PieceMask.WHITE_SHORT_SQUARE_HOLE
    | PieceMask.WHITE_SHORT_SQUARE_SOLID
    | PieceMask.WHITE_TALL_CIRCLE_SOLID
    | PieceMask.WHITE_TALL_SQUARE_HOLE
    | PieceMask.WHITE_TALL_SQUARE_SOLID
)

BLACK_PIECES: int = (
    PieceMask.BLACK_TALL_CIRCLE_HOLE 
    | PieceMask.BLACK_SHORT_CIRCLE_HOLE
    | PieceMask.BLACK_SHORT_CIRCLE_SOLID
    | PieceMask.BLACK_SHORT_SQUARE_HOLE
    | PieceMask.BLACK_SHORT_SQUARE_SOLID
    | PieceMask.BLACK_TALL_CIRCLE_SOLID
    | PieceMask.BLACK_TALL_SQUARE_HOLE
    | PieceMask.BLACK_TALL_SQUARE_SOLID
)

class Winner(IntEnum):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 3

class State(NamedTuple):
    board: tuple[tuple[int, ...], ...]
    remaining_pieces: int   # Each bit represents having a piece (1) or not having a piece (0)
                            # 0xFFFF to start, P1 has white pieces, P2 has black pieces
    given_piece: int # The piece given to the opposite player of the player whose turn it is

class ActionPlace(NamedTuple):
    """ Describes where the given piece should be placed """
    row: int
    col: int

class ActionGive(NamedTuple):
    """ Describes which piece to give """
    piece: int