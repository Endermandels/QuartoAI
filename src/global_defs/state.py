from enum import IntEnum
from typing import NamedTuple

class PiecePlace(IntEnum):
    """ Defines pieces based on category: b3 = white/black, b2 = tall/short, b1 = square/circle, b0 = hole/solid """
    EMPTY = 0x10
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

class State(NamedTuple):
    board: tuple[tuple[int, ...], ...]
    remaining_pieces: int   # Each bit represents having a piece (1) or not having a piece (0)
                            # P1 has white pieces, P2 has black pieces
    given_piece: int # The piece given to the opposite player of the player whose turn it is

class Action(NamedTuple):
    board_coords: tuple[int, int] = (-1, -1)
    piece: int = PieceGive.EMPTY.value