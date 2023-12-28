from Data import *
import pygame
from files import find_piece_image
import random



def pos_to_coords(pos: str) -> (int, int):
    return lookup[pos[0]] * SIZE - SIZE/2, lookup[pos[1]] * SIZE - SIZE/2
def coords_to_pos(coords: (int, int)) -> str:
    return rows[int(coords[0]//SIZE)] + col[int(coords[1]//SIZE)]


def mouse_to_square(just_coords = False):
    mouse_pos = pygame.mouse.get_pos()
    clamped_x, clamped_y = max(10, min(mouse_pos[0], WIDTH-10)), max(10, min(mouse_pos[1], HEIGHT-10))
    if just_coords:
        return clamped_x, clamped_y
    else:
        return coords_to_pos((clamped_x, clamped_y))
class Board:
    def __init__(self):
        def tile_vals(n, i):
            return Tile((n*SIZE, i* SIZE), (LIGHT if ((n+i)%2==0) else DARK))
        def tile_keys(i):
            return rows[i//8] + col[i%8]

        self.group = pygame.sprite.Group()
        self.tiles = {tile_keys(i):[tile_vals(i//8,i%8), None] for i in range(64)}
        self.pieces = []
        self.surface = pygame.display.get_surface()
        for item in start:
            self.tiles[item[1]][1] = (Piece(item[0], item[1], item[2]))


    def render(self):
        for tile in self.tiles.values():
            self.surface.blit(tile[0].image, tile[0].rect)
            if tile[1] is not None:
                self.surface.blit(tile[1].image, tile[1].rect)

class Tile:
    def __init__(self, position:(int, int), col: pygame.Color) -> None:

        self.image = pygame.Surface((SIZE,SIZE))
        self.col = col
        self.image.fill(self.col)

        self.rect = self.image.get_rect()
        print(position)
        self.rect.move_ip(position[0], position[1])

    def highlight(self, color):
        new_col = self.col.lerp(color, 0.3)
        self.image.fill(new_col)
    def remove_highlight(self):
        self.image.fill(self.col)

class Piece:
    def __init__(self, type: str ,position: str, color: str, moves = 0, stat = False) -> None:
        self.captured = False
        self.position = position
        self.color = color
        self.type = type
        self.image = pygame.image.load(find_piece_image(type, color))
        self.image = pygame.transform.smoothscale(self.image.convert_alpha(), (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos_to_coords(position)

        #Enpassant + Castle params
        self.moves = moves
        self.stat = stat


class Player:
    def __init__(self, board: Board, color: str) -> None:
        self.board = board
        self.color = color
        self.piece = None
        self.surface = pygame.display.get_surface()

        #For moving pieces
        self.valid_positions = [*self.board.tiles]
        self.go_back = 'A1'

    def pickup(self) -> Piece: #Picks up piece at current square and returns piece
        pos = mouse_to_square()
        to_lift = self.board.tiles[pos][1]
        self.go_back = pos
        if to_lift is not None and to_lift.color == self.color:
            self.piece = to_lift
            self.board.tiles[pos][1] = None
        return self.piece

    def put_down(self) -> bool: #Puts down piece, returns True if the piece is in a new position
        pos = mouse_to_square()
        if pos in self.valid_positions:
            self.board.tiles[pos][1] = Piece(self.piece.type, pos, self.piece.color, self.piece.moves + 1)
            print(self.piece.moves)
            ret_val = True
        else:
            self.board.tiles[self.go_back][1] = Piece(self.piece.type, self.go_back, self.piece.color)
            ret_val = False
        self.piece = None
        #self.valid_positions = random.choice([*self.board.tiles])
        return ret_val

    def display_motion(self) -> None:
        if self.piece is not None:
            self.piece.rect.center = mouse_to_square(True)
            self.surface.blit(self.piece.image, self.piece.rect)

    def mouse_over(self):
        for tile in self.board.tiles.values():
            tile[0].remove_highlight()

        square = mouse_to_square()
        self.board.tiles[square][0].highlight('brown')








