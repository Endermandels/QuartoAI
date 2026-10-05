from enum import IntEnum
from typing import NamedTuple

PIECES_FULL = 0xFF # All pieces available

class PieceMask(IntEnum):
    """ Mask for piece available for player to hand over """
    TALL_SQUARE_HOLE = 0x01
    TALL_SQUARE_SOLID = 0x02
    TALL_CIRCLE_HOLE = 0x04
    TALL_CIRCLE_SOLID = 0x08
    SHORT_SQUARE_HOLE = 0x10
    SHORT_SQUARE_SOLID = 0x20
    SHORT_CIRCLE_HOLE = 0x40
    SHORT_CIRCLE_SOLID = 0x80

class BoardSpace(IntEnum):
    """ Board space contents """
    WHITE_TALL_SQUARE_HOLE = 0
    WHITE_TALL_SQUARE_SOLID = 1
    WHITE_TALL_CIRCLE_HOLE = 2
    WHITE_TALL_CIRCLE_SOLID = 3
    WHITE_SHORT_SQUARE_HOLE = 4
    WHITE_SHORT_SQUARE_SOLID = 5
    WHITE_SHORT_CIRCLE_HOLE = 6
    WHITE_SHORT_CIRCLE_SOLID = 7
    BLACK_TALL_SQUARE_HOLE = 8
    BLACK_TALL_SQUARE_SOLID = 9
    BLACK_TALL_CIRCLE_HOLE = 10
    BLACK_TALL_CIRCLE_SOLID = 11
    BLACK_SHORT_SQUARE_HOLE = 12
    BLACK_SHORT_SQUARE_SOLID = 13
    BLACK_SHORT_CIRCLE_HOLE = 14
    BLACK_SHORT_CIRCLE_SOLID = 15
    EMPTY = 16

class Winner(IntEnum):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 3

class State(NamedTuple):
    board: tuple[tuple[int, ...], ...]
    p1_pieces: int # Each bit represents having a piece (1) or not having a piece (0)
    p2_pieces: int # 0xFF to start, P1 has white pieces, P2 has black pieces
    given_piece: int # The piece given to the opposite player of the player whose turn it is
    is_p1_turn: bool
    winner: int

class ActionPlace(NamedTuple):
    """ Describes where the given piece should be placed """
    row: int
    col: int

class ActionGive(NamedTuple):
    """ Describes which piece to give """
    piece: PieceMask