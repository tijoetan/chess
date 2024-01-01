import Data
from Board import Board, Piece
from copy import copy, deepcopy


def place_piece(tiles: dict, position, piece):
    to_change = tiles
    to_change[piece.position][1] = Piece(piece.type, position, piece.color, piece.moves + 1)
    return to_change


def shift_piece(tiles, start_pos, end_pos):
    to_shift = tiles[start_pos][1]
    if to_shift is not None:
        tiles[end_pos][1] = Piece(to_shift.type, end_pos, to_shift.color, to_shift.moves + 1)
        tiles[start_pos][1] = None
    print(tiles)
    return tiles


def apply_move(tiles: dict, move, piece: Piece, way='place') -> Board:  # Either piece is given to be placed
    # or start square is given to move piece
    new_tiles = tiles.copy()
    new_piece = copy(piece)
 
    position = move[0:2]
    flags = move[2:]

    if 'c' in flags:  # Castling
        king_move = place_piece(new_tiles, position, new_piece)
        col_ind = Data.cols.index(position[0])
        castle_type = 'R' if col_ind > 5 else 'L'
        rook_start = ('H' if castle_type == 'R' else 'A') + position[1]
        rook_end = (Data.cols[col_ind - 1] if castle_type == 'R' else Data.cols[col_ind + 1]) + position[1]
        return shift_piece(king_move, rook_start, rook_end)

    if 'e' in flags:
        passant = place_piece(new_tiles, position, new_piece)
        to_capture = position[0] + (position[1] - 1 if piece.color == 'white' else position[1] + 1)
        new_tiles[to_capture][1] = None
        return new_tiles
    else:
        if way == 'shift':
            return shift_piece(new_tiles, new_piece.position, position)
        else:
            return place_piece(new_tiles, position, new_piece) # if piece is not None else shift_piece(to_move, move)
