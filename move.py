import Data
from Board import Board, Piece


def place_piece(tiles: dict, position, piece, return_piece = False):
    tiles[piece.position][1] = Piece(piece.type, position, piece.color, piece.moves + 1)
    return tiles


def shift_piece(tiles, start_pos, end_pos, return_piece = False):
    to_shift = tiles[start_pos][1]
    if to_shift is not None:
        tiles[end_pos][1] = Piece(to_shift.type, end_pos, to_shift.color, to_shift.moves + 1)
        tiles[start_pos][1] = None
    print(tiles)
    return tiles


def apply_move(tiles: dict, move, piece: Piece, return_piece = False) -> Board:  # Either piece is given to be placed
    # or start square is given to move piece

    position = move[0:2]
    flags = move[2:]

    if 'c' in flags:  # Castling
        king_move = place_piece(tiles, position, piece)
        col_ind = Data.cols.index(position[0])
        castle_type = 'R' if col_ind > 5 else 'L'
        rook_start = ('H' if castle_type == 'R' else 'A') + position[1]
        rook_end = (Data.cols[col_ind - 1] if castle_type == 'R' else Data.cols[col_ind + 1]) + position[1]
        return shift_piece(king_move, rook_start, rook_end)

    if 'e' in flags:
        passant = place_piece(tiles, position, piece)
        to_capture = position[0] + (position[1] - 1 if piece.color == 'white' else position[1] + 1)
        tiles[to_capture][1] = None
        return tiles
    else:
        return place_piece(tiles, position, piece) # if piece is not None else shift_piece(to_move, move)
