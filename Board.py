import Data
from Data import *
import pygame
from files import find_piece_image


def pos_to_coords(pos: str) -> (int, int):
    return lookup[pos[0]] * SIZE - SIZE / 2, lookup[pos[1]] * SIZE - SIZE / 2


def coords_to_pos(coords: (int, int)) -> str:
    return cols[int(coords[0] // SIZE)] + rows[int(coords[1] // SIZE)]


def mouse_to_square(just_coords=False):
    mouse_pos = pygame.mouse.get_pos()
    clamped_x, clamped_y = max(10, min(mouse_pos[0], WIDTH - 10)), max(10, min(mouse_pos[1], HEIGHT - 10))
    if just_coords:
        return clamped_x, clamped_y
    else:
        return coords_to_pos((clamped_x, clamped_y))


class Board:
    def __init__(self):
        def tile_vals(n, i):
            return Tile((n * SIZE, i * SIZE), (LIGHT if ((n + i) % 2 == 0) else DARK))

        def tile_keys(i):
            return cols[i // 8] + rows[i % 8]

        self.group = pygame.sprite.Group()
        self.tiles = {tile_keys(i): [tile_vals(i // 8, i % 8), None] for i in range(64)}
        self.surface = pygame.display.get_surface()
        self.lopieces = []
        for item in start:
            piece = Piece(item[0], item[1], item[2])
            self.tiles[item[1]][1] = piece
            self.lopieces.append(piece)

    def render(self):
        for tile in self.tiles.values():
            self.surface.blit(tile[0].image, tile[0].rect)
            if tile[1] is not None:
                self.surface.blit(tile[1].image, tile[1].rect)

    def copy_tiles(self):
        copy = {}
        for key in self.tiles:
            piece = self.tiles[key][1]
            copy[key] = [piece.type, piece.position, piece.color] if piece is not None else None


class Tile:
    def __init__(self, position: (int, int), col: pygame.Color, surf_source) -> None:
        # for copy
        self.position = position
        self.col = col

        self.surf_source = surf_source
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(self.col)

        self.rect = pygame.Rect(0, 0, Data.SIZE, Data.SIZE)  # self.image.get_rect()
        # print(position)
        self.rect.move_ip(position[0], position[1])

    def highlight(self, color):
        new_col = self.col.lerp(color, 0.3)
        self.surf_source = f"{self.col}_highlight"
        self.image.fill(new_col)

    def remove_highlight(self):
        self.surf_source = self.col
        self.image.fill(self.col)


class Piece:
    def __init__(self, type: str, position: str, color: str, moves=0, stat=False) -> None:
        self.captured = False
        self.position = position
        self.color = color
        self.type = type
        self.image = pygame.image.load(find_piece_image(type, color))
        self.image = pygame.transform.smoothscale(self.image.convert_alpha(), (SIZE, SIZE))
        self.rect = pygame.Rect(0, 0, SIZE, SIZE)
        self.rect.centerx, self.rect.centery = pos_to_coords(position)

        # Enpassant + Castle params
        self.moves = moves
        self.stat = stat


def copy_tiles(tiles: dict[str:[Tile, Piece]]):
    copy = {}
    for tile_key in tiles:
        tile = tiles[tile_key][0]
        piece = tiles[tile_key][1]
        copy[tile_key] = [Tile(tile.position, tile.col), (Piece(piece.type, piece.position, piece.color)
                                                          if piece is not None else None)]
    return copy
