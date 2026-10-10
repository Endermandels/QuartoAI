from enum import IntEnum
from typing import NamedTuple

class PiecePlace(IntEnum):
    """ Defines pieces based on category: b3 = white/black, b2 = tall/short, b1 = square/circle, b0 = hole/solid """
    WHITE_TALL_SQUARE_HOLE = 0x0
    WHITE_TALL_SQUARE_SOLID = 0x1
    WHITE_TALL_CIRCLE_HOLE = 0x2
    WHITE_TALL_CIRCLE_SOLID = 0x3
    WHITE_SHORT_SQUARE_HOLE = 0x4
    WHITE_SHORT_SQUARE_SOLID = 0x5
    WHITE_SHORT_CIRCLE_HOLE = 0x6
    WHITE_SHORT_CIRCLE_SOLID = 0x7
    BLACK_TALL_SQUARE_HOLE = 0x8
    BLACK_TALL_SQUARE_SOLID = 0x9
    BLACK_TALL_CIRCLE_HOLE = 0xA
    BLACK_TALL_CIRCLE_SOLID = 0xB
    BLACK_SHORT_SQUARE_HOLE = 0xC
    BLACK_SHORT_SQUARE_SOLID = 0xD
    BLACK_SHORT_CIRCLE_HOLE = 0xE
    BLACK_SHORT_CIRCLE_SOLID = 0xF

class PieceGive(IntEnum):
    """ Mask for pieces stored in state.remaining_pieces """
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
    PieceGive.WHITE_TALL_CIRCLE_HOLE 
    | PieceGive.WHITE_SHORT_CIRCLE_HOLE
    | PieceGive.WHITE_SHORT_CIRCLE_SOLID
    | PieceGive.WHITE_SHORT_SQUARE_HOLE
    | PieceGive.WHITE_SHORT_SQUARE_SOLID
    | PieceGive.WHITE_TALL_CIRCLE_SOLID
    | PieceGive.WHITE_TALL_SQUARE_HOLE
    | PieceGive.WHITE_TALL_SQUARE_SOLID
)

BLACK_PIECES: int = (
    PieceGive.BLACK_TALL_CIRCLE_HOLE 
    | PieceGive.BLACK_SHORT_CIRCLE_HOLE
    | PieceGive.BLACK_SHORT_CIRCLE_SOLID
    | PieceGive.BLACK_SHORT_SQUARE_HOLE
    | PieceGive.BLACK_SHORT_SQUARE_SOLID
    | PieceGive.BLACK_TALL_CIRCLE_SOLID
    | PieceGive.BLACK_TALL_SQUARE_HOLE
    | PieceGive.BLACK_TALL_SQUARE_SOLID
)

class Winner(IntEnum):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 3

ALL_EMPTY = 0xFFFF
GRID_LEN = 4
PIECE_SIZE = 4 # number of bits per piece
PIECE_MASK = 0xF

class State(NamedTuple):
    board: int # each nibble is a space (16 spaces, 4 bits per space, 64 bits total)
    empty: int # each bit is an empty space on board (16 spaces, 1 bit per space, 16 bits total)
    remaining_pieces: int   # each bit is a remaining piece (16 pieces, 1 bit per piece, 16 bits total)
    given_piece: int # The piece given to the opposite player of the player whose turn it is (4 bits)

class Action(NamedTuple):
    space: int = 0x10 # each value is a space (16 spaces, 16 values), 0x10 = Empty
    piece: int = PieceGive.EMPTY.value