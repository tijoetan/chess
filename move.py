import Data
from Board import Board, Piece


def place_piece(board, position, piece) -> Board:
    board[piece.position][1] = Piece(piece.type, position, piece.color, piece.moves + 1)
    return board


def shift_piece(board, start_pos, end_pos):
    to_shift = board[start_pos][1]
    board[end_pos][1] = Piece(to_shift.type, end_pos, to_shift.color, to_shift.moves + 1)
    board[start_pos][1] = None
    return board


def apply_move(board: Board, move, piece: Piece) -> Board:  # Either piece is given to be placed
    # or start square is given to move piece
    new_board = board.tiles

    position = move[0:2]
    flags = move[2:]

    if 'c' in flags:  # Castling
        king_move = place_piece(new_board, position, piece)
        col_ind = Data.cols.index(position[0])
        castle_type = 'R' if col_ind > 5 else 'L'
        rook_start = ('H' if castle_type == 'R' else 'A') + position[1]
        rook_end = (Data.cols[col_ind - 1] if castle_type == 'R' else Data.cols[col_ind + 1]) + position[1]
        return shift_piece(king_move, rook_start, rook_end)

    if 'e' in flags:
        passant = place_piece(new_board, position, piece)
        to_capture = position[0] + (position[1] - 1 if piece.color == 'white' else position[1] + 1)
        new_board[to_capture][1] = None
        return new_board
    else:
        return place_piece(new_board, position, piece)  # if piece is not None else shift_piece(to_move, move)
