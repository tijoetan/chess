import Data
from Board import Board, Piece
import pygame
pygame.init()
pygame.display.set_mode((200,200))

def check_check(king: Piece, board: Board) -> bool: #Determines if given king is in check
    return
def king_fn(piece:Piece, board:Board):
    row_ind, col_ind = Data.rows.index(piece.position[0]), Data.cols.index(piece.position[1])
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
# return result

print(king_fn(Piece('king', 'E1', 'white'), Board()))
def queen_fn(piece: Piece, board:Board):
    return 5

def pawn_fn(piece: Piece, board:Board):
    return 4

def bishop_fn(piece: Piece, board:Board):
    return 3

def knight_fn(piece: Piece, board:Board):
    return 2

def rook_fn(piece: Piece, board:Board):
    return 1

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
        moves[piece] = []
        for candidate in opts[piece.type](piece, board):
            moves[piece].append(candidate)
    return moves

print(get_moves(Board(), 'white'))