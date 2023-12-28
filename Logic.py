from Board import Board, Piece


def king_fn(piece: Piece, board:Board):
    return 6

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
def get_valid_pos(piece: Piece, board:Board) -> list[str]:
    return opts[piece](piece, board)


print(get_valid_pos('rook', 2))