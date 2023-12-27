from Data import *
import pygame
from files import find_piece_image

def gen_squares():
    letters = {"A"}
    board = [[('B' if ((n+i)%2==0) else 'W') for n in range(8)] for i in range(8)]
    return board


def pos_to_coords(pos: str) -> (int, int):
    return lookup[pos[0]] * SIZE - SIZE/2, lookup[pos[1]] * SIZE - SIZE/2
def coords_to_pos(coords: (int, int)) -> str:
    return rows[int(coords[0]//SIZE)] + col[int(coords[1]//SIZE)]
def mouse_to_square():
    mouse_pos = pygame.mouse.get_pos()
    return coords_to_pos(mouse_pos)
class Board:
    def __init__(self):
        def tile_vals(n, i):
            return Tile(self.group,(n*SIZE, i* SIZE), (LIGHT if ((n+i)%2==0) else DARK))
        def tile_keys(i):
            return rows[i//8] + col[i%8]

        self.group = pygame.sprite.Group()
        self.tiles = {tile_keys(i):[tile_vals(i//8,i%8), None] for i in range(64)}
        self.pieces = []
        for item in start:
            self.tiles[item[1]][1] = (Piece(item[0], item[1], item[2]))


    def render(self):
        surface = pygame.display.get_surface()
        for tile in self.tiles.values():
            surface.blit(tile[0].image, tile[0].rect)
            if tile[1] is not None:
                surface.blit(tile[1].image, tile[1].rect)

class Tile:
    def __init__(self, group:pygame.sprite.Group, position:(int, int), col: pygame.Color) -> None:

        self.image = pygame.Surface((SIZE,SIZE))
        self.col = col
        self.image.fill(self.col)

        self.rect = self.image.get_rect()
        print(position)
        self.rect.move_ip(position[0], position[1])

    def highlight(self, col):
        new_col = self.col.lerp(col, 0.3)
        self.image.fill(new_col)
    def remove_highlight(self):
        self.image.fill(self.col)

class Piece:
    def __init__(self, type: str ,position: str, color: str) -> None:
        self.captured = False
        self.position = position
        self.color = color
        self.image = pygame.image.load(find_piece_image(type, color))
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos_to_coords(position)


class Player:
    def __init__(self, board: Board, color: str):
        self.board = board
        self.color = color
        self.piece = []

    def get_click(self):
        for tile in self.board.tiles.values():
            tile[0].remove_highlight()

        square = mouse_to_square()
        self.board.tiles[square][0].highlight('red')



