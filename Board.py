from Data import *
import pygame
from files import find_piece_image

def pos_to_coords(pos: str) -> (int, int):
    return lookup[pos[0]] * SIZE - SIZE/2, lookup[pos[1]] * SIZE - SIZE/2
def coords_to_pos(coords: (int, int)) -> str:
    return rows[int(coords[0]//SIZE)] + cols[int(coords[1] // SIZE)]


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
            return rows[i//8] + cols[i % 8]

        self.group = pygame.sprite.Group()
        self.tiles = {tile_keys(i):[tile_vals(i//8,i%8), None] for i in range(64)}
        self.surface = pygame.display.get_surface()
        self.lopieces = []
        for item in start:
            piece = Piece(item[0], item[1], item[2])
            self.tiles[item[1]][1] = piece
            self.lopieces.append(piece)

    def apply_move(self, move, piece=None, to_move=None):  #Either piece is given to be placed
                                                           # or start square is given to move piece
        new_board = self.tiles.copy()
        def place_piece(piece: Piece, position: str) -> Board:
            new_board[position][1] = Piece(piece.type, position, piece.color, piece.moves + 1)
            return new_board
        def shift_piece(start_pos, end_pos):
            to_shift = new_board[start_pos][1]
            new_board[end_pos][1] =  Piece(to_shift.type, end_pos, to_shift.color, to_shift.moves + 1)
            new_board[start_pos][1] = None
            return new_board
        return place_piece(piece, move) if piece is not None else shift_piece(to_move,move)



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
        #print(position)
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