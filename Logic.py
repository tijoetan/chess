import Data
from Board import Board, Piece, copy_tiles
from move import apply_move
from copy import copy, deepcopy
import pygame


def get_index(position: str) -> (int, int):
    return Data.cols.index(position[0]), Data.rows.index(position[1])


def get_vertical(row_ind, col_ind):
    return


def king_fn(piece: Piece, tiles: dict) -> list[str]:
    row_ind, col_ind = get_index(piece.position)
    new_cols = [Data.rows[col_ind + i] for i in range(-1, 2) if col_ind + i in range(0, 8)]
    new_rows = [Data.cols[row_ind + i] for i in range(-1, 2) if row_ind + i in range(0, 8)]
    for row in new_rows:
        for col in new_cols:
            if row + col == piece.position:
                continue
            elif tiles[row + col][1] is not None:
                if tiles[row + col][1].color == piece.color:
                    continue
                else:
                    yield row + col + 'x'
            else:
                yield row + col
    if piece.moves == 0:
        horizontals = [Data.cols[:row_ind][::-1], Data.cols[row_ind + 1:]]
        # print(horizontals)
        row = piece.position[1]
        for lr in horizontals:
            for col in lr:
                tile = tiles[col + row][1]
                if tile is None:
                    # print('empty square')
                    continue
                elif tile.type == 'rook' and tile.moves == 0:
                    yield lr[1] + row + 'c'
                else:
                    break


def queen_fn(piece: Piece, tiles: dict):
    for diagonal in bishop_fn(piece, tiles):
        yield diagonal
    for linear in rook_fn(piece, tiles):
        yield linear


def pawn_fn(piece: Piece, tiles: dict) -> list[str]:
    row_ind, col_ind = get_index(piece.position)
    direction = -1 if piece.color == 'white' else 1
    order = Data.rows[::(-1*direction)]
    max = order[0]
    passant_row = order[3]
    capture_row = order[2]
    print(piece.position)
    print(capture_row)
    advance_one = False
    new_pos = [Data.cols[row_ind + i] + Data.rows[col_ind + direction]
               for i in range(-1, 2) if row_ind + i in range(0, 8)]
    # print(new_pos)
    for pos in new_pos:
        to_promote = (pos[1] == max)
        prom_flag = 'p' if to_promote else ''
        if pos[0] == piece.position[0] and tiles[pos][1] is None:
            advance_one = True
            yield pos + prom_flag

        elif (tiles[pos][1] is not None and
              tiles[pos][1].color != piece.color and
              pos[0] != piece.position[0]):

            yield pos + 'x' + prom_flag
        elif pos[1] == capture_row:
            to_capture = tiles[pos[0] + passant_row][1]
            if to_capture is not None and to_capture.type == 'pawn' and not to_capture.stat and to_capture.moves == 1:
                yield pos + 'e'
    if piece.moves == 0 and advance_one:
        double_spot = tiles[piece.position[0] + Data.rows[col_ind + 2 * direction]][1]
        if double_spot is None:
            yield piece.position[0] + Data.rows[col_ind + 2 * direction]

    # NEED en passant and promotion


def bishop_fn(piece: Piece, tiles: dict) -> list[str]:
    row_ind, col_ind = get_index(piece.position)
    vertical = [Data.rows[:col_ind][::-1], Data.rows[col_ind + 1:]]
    horizontal = [Data.cols[:row_ind][::-1], Data.cols[row_ind + 1:]]
    for vert in vertical:
        for hori in horizontal:
            for direction in zip(hori, vert):
                to_check = tiles[direction[0] + direction[1]][1]
                if to_check is not None:
                    if to_check.color != piece.color:
                        yield direction[0] + direction[1] + 'x'
                    break
                else:
                    yield direction[0] + direction[1]


def knight_fn(piece: Piece, tiles: dict) -> list[str]:
    row_ind, col_ind = get_index(piece.position)
    verticals = [[Data.rows[col_ind + 2 * i] for i in range(-1, 2, 2) if col_ind + 2 * i in range(0, 8)]]
    horizontals = [[Data.cols[row_ind + 2 * i] for i in range(-1, 2, 2) if row_ind + 2 * i in range(0, 8)]]

    for direction in verticals + horizontals:
        for step in direction:
            if direction in verticals:
                left = Data.cols[row_ind + 1] + step if row_ind + 1 in range(0, 8) else None
                right = Data.cols[row_ind - 1] + step if row_ind - 1 in range(0, 8) else None
                if left is not None:
                    if tiles[left][1] is None:
                        yield left
                    elif tiles[left][1].color != piece.color:
                        yield left + 'x'
                if right is not None:
                    if tiles[right][1] is None:
                        yield right
                    elif tiles[right][1].color != piece.color:
                        yield right + 'x'
            else:
                up = step + Data.rows[col_ind + 1] if col_ind + 1 in range(0, 8) else None
                down = step + Data.rows[col_ind - 1] if col_ind - 1 in range(0, 8) else None
                if up is not None:
                    if tiles[up][1] is None:
                        yield up
                    elif tiles[up][1].color != piece.color:
                        yield up + 'x'
                if down is not None:
                    if tiles[down][1] is None:
                        yield down
                    elif tiles[down][1].color != piece.color:
                        yield down + 'x'


def rook_fn(piece: Piece, tiles: dict) -> list[str]:
    row_ind, col_ind = get_index(piece.position)
    vertical = [Data.rows[:col_ind][::-1], Data.rows[col_ind + 1:]]
    horizontal = [Data.cols[:row_ind][::-1], Data.cols[row_ind + 1:]]
    for directions in vertical + horizontal:
        for direction in directions:
            pos = piece.position[0] + direction if directions in vertical else direction + piece.position[1]
            to_check = tiles[pos][1]
            if to_check is not None:
                if to_check.color != piece.color:
                    yield pos + 'x'
                break
            else:
                yield pos


opts = {'king': king_fn, 'queen': queen_fn, 'rook': rook_fn, 'bishop': bishop_fn, 'pawn': pawn_fn, 'knight': knight_fn}


def get_danger(col_king: Piece, board: dict):
    col = 'black' if col_king.color == 'white' else 'white'
    result = []
    for move in queen_fn(Piece('king', col_king.position, col), board):
        result.append(move[0:2])
    return result


def check_check(king: Piece, board: dict) -> bool:  # Determines if given king is in check
    for fn in zip(opts.values(), opts.keys()):
        # if fn[1] == 'king':
        #     continue
        # else:
        for move in fn[0](king, board):
            piece = board[move[0:2]][1]
            if piece is not None and piece.color != king.color and piece.type == fn[1]:
                return True
    return False


def get_moves(board: Board, col: str) -> dict[Piece:list[str]]:
    moves = {}
    col_pieces, enm_pieces = [], []
    col_king = None
    no_moves = True
    for tile in board.tiles.values():
        if tile[1] is not None:
            if tile[1].color == col:
                tile[1].stat = True
                col_pieces.append(tile[1])
                if tile[1].type == 'king':
                    col_king = tile[1]
            else:
                enm_pieces.append(tile[1])
    danger_spots = get_danger(col_king, board.tiles)
    print(danger_spots)
    checked = check_check(col_king, board.tiles)
    for piece in col_pieces:
        moves[piece.position] = [[], []]  # Stores position and special flags respectively
        for candidate in opts[piece.type](piece, board.tiles):
            if piece.position in danger_spots or piece.type == 'king' or checked:
                test_board = copy_tiles(board.tiles)
                test_piece = copy(piece)
                test_board[piece.position][1] = None
                test_piece.position = candidate[0:2]
                if check_check(test_piece if piece.type == 'king' else col_king,
                               apply_move(test_board, candidate, test_piece)):
                    continue

            moves[piece.position][0].append(candidate[0:2])
            moves[piece.position][1].append(candidate[2:])
            no_moves = False
    if no_moves:
        if checked:
            return 1
        else:
            return 2
    return moves

# print(get_moves(Board(), 'black'))
