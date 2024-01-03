import pygame

from Board import Board, Piece, mouse_to_square
from Logic import get_moves
from move import apply_move


class Player:
    def __init__(self, board: Board, color: str) -> None:
        self.board = board
        self.color = color
        self.held_piece = None
        self.surface = pygame.display.get_surface()

        # For moving pieces
        self.valid_moves = [[], []]
        self.go_back = ''
        self.move_dict = {}
        self.highlight_col = 'purple' if color == 'white' else 'green'

    def pickup(self) -> Piece:  # Picks up piece at current square and returns piece
        pos = mouse_to_square()
        to_lift = self.board.tiles[pos][1]
        self.go_back = pos
        if to_lift is not None and to_lift.color == self.color:
            self.held_piece = to_lift
            self.board.tiles[pos][1] = None
            self.valid_moves = self.move_dict[pos]
        return self.held_piece

    def put_down(self) -> bool:  # Puts down piece, returns True if the piece is in a new position
        pos = mouse_to_square()
        if pos in self.valid_moves[0]:
            flags = self.valid_moves[1][self.valid_moves[0].index(pos)]
            # x = input('what would you like to promote to')
            # print('fe')
            # updated_piece = Piece(x, pos, self.held_piece.color, self.held_piece.moves + 1
            self.held_piece = Piece(self.held_piece.type, pos, self.held_piece.color, self.held_piece.moves)
            did_move = True
            self.board.tiles = apply_move(self.board.tiles, pos + flags if flags is not None else pos,
                                          self.held_piece)
            if 'p' in flags and self.held_piece.type == 'pawn':
                raise KeyError('must promote')
        else:
            self.board.tiles[self.go_back][1] = Piece(self.held_piece.type, self.go_back,
                                                      self.held_piece.color, self.held_piece.moves)
            did_move = False
        self.held_piece = None
        # self.valid_positions = random.choice([*self.board.tiles])
        return did_move

    def move_lifted(self) -> None:
        if self.held_piece is not None:
            self.held_piece.rect.center = mouse_to_square(True)
            # self.surface.blit(self.held_piece.image, self.held_piece.rect)

    def color_tiles(self):
        for tile in zip(self.board.tiles.keys(), self.board.tiles.values()):
            tile[1][0].remove_highlight()
            if tile[0] in self.valid_moves[0]:
                index = self.valid_moves[0].index(tile[0])
                if 'x' in self.valid_moves[1][index]:
                    tile[1][0].highlight('capture')
                else:
                    tile[1][0].highlight('accepted')
        if self.held_piece is None:
            square = mouse_to_square()
            self.board.tiles[square][0].highlight('hover')

    def update_moves(self) -> dict or None:
        self.move_dict = get_moves(self.board, self.color)
        if self.move_dict in [1, 2]:
            return self.move_dict
        self.valid_moves = [[], []]
        print(self.move_dict)
        return
