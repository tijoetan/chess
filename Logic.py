import Data
from Board import Board, Piece
import pygame

def get_index(position):
    return Data.rows.index(position[0]), Data.cols.index(position[1])
def check_check(king: Piece, board: Board) -> bool: #Determines if given king is in check

    return
def king_fn(piece:Piece, board:Board):
    row_ind, col_ind = get_index(piece.position)
    new_cols = [Data.cols[col_ind + i] for i in range(-1, 2) if col_ind + i in range(0, 8)]
    new_rows = [Data.rows[row_ind+i] for i in range(-1, 2) if row_ind + i in range(0,8)]
    result = []
    for row in new_rows:
        for col in new_cols:
            if row + col == piece.position:
                continue
            elif board.tiles[row + col][1] is not None and board.tiles[row + col][1].color == piece.color:
                continue
            else:
                yield row+col
        # NEED castling

def queen_fn(piece: Piece, board:Board):
    for diagonal in bishop_fn(piece, board):
        yield diagonal
    for linear in rook_fn(piece, board):
        yield linear

def pawn_fn(piece: Piece, board:Board):
    row_ind, col_ind = get_index(piece.position)
    direction = -1 if piece.color == 'white' else 1
    advance_one = False
    new_pos = [Data.rows[row_ind + i] + Data.cols[col_ind + direction]
               for i in range(-1, 2) if row_ind + i in range(0,8)]
    #print(new_pos)
    for pos in new_pos:
        if pos[0] == piece.position[0] and board.tiles[pos][1] is None:
            advance_one = True
            yield pos
        elif board.tiles[pos][1] is not None and board.tiles[pos][1].color != piece.color:
            yield pos
    double_spot = board.tiles[piece.position[0] + Data.cols[col_ind + 2*direction]][1]
    if piece.moves == 0 and double_spot is None and advance_one:
        yield piece.position[0] + Data.cols[col_ind + 2*direction]

    # NEED en passant and promotion
def bishop_fn(piece: Piece, board:Board):
    row_ind, col_ind = get_index(piece.position)
    vertical = [Data.cols[:col_ind][::-1], Data.cols[col_ind+1:]]
    horizontal = [Data.rows[:row_ind][::-1], Data.rows[row_ind+1:]]
    for vert in vertical:
        for hori in horizontal:
            for direction in zip(hori, vert):
                to_check = board.tiles[direction[0] + direction[1]][1]
                if to_check is not None:
                    if to_check.color != piece.color:
                        yield direction[0] + direction[1]
                    break
                else:
                    yield direction[0] + direction[1]


def knight_fn(piece: Piece, board:Board):
    return []

def rook_fn(piece: Piece, board:Board):
    row_ind, col_ind = get_index(piece.position)
    vertical = [Data.cols[:col_ind][::-1], Data.cols[col_ind + 1:]]
    horizontal = [Data.rows[:row_ind][::-1], Data.rows[row_ind + 1:]]
    for directions in vertical:
        for direction in directions:
            to_check = board.tiles[piece.position[0] + direction][1]
            if to_check is not None:
                if to_check.color != piece.color:
                    yield piece.position[0] + direction
                break
            else:
                yield piece.position[0] + direction

    for directions in horizontal:
        for direction in directions:
            to_check = board.tiles[direction + piece.position[1]][1]
            if to_check is not None:
                if to_check.color != piece.color:
                    yield direction + piece.position[1]
                break
            else:
                yield direction + piece.position[1]

opts = {'king':king_fn, 'queen': queen_fn, 'rook':rook_fn, 'bishop':bishop_fn, 'pawn':pawn_fn, 'knight': knight_fn}
def get_moves(board:Board, col: str) -> dict[Piece:list[str]]:
    moves = {}
    col_pieces, enm_pieces = [], []
    col_king, enm_king = None, None
    for tile in board.tiles.values():
        if tile[1] is not None:
            if tile[1].color == col:
                col_pieces.append(tile[1])
                if tile[1].type == 'king':
                    col_king = tile[1]
            else:
                enm_pieces.append(tile[1])
                if tile[1].type == 'king':
                    enm_king = tile[1]

    for piece in col_pieces:
        moves[piece.position] = []
        for candidate in opts[piece.type](piece, board):
            moves[piece.position].append(candidate)
    return moves

#print(get_moves(Board(), 'black'))