import pygame
from files import find_piece_image

WIDTH = 8 * 60
HEIGHT = WIDTH
LIGHT = pygame.Color(240, 217, 181)
DARK = pygame.Color(181, 136, 99)

DARK_HOVER = DARK.lerp('red', 0.3)
LIGHT_HOVER = LIGHT.lerp('red', 0.3)

SIZE = int(WIDTH // 8)

cols = 'ABCDEFGH'
rows = '87654321'
lookup = {'A': 1, "1": 8, 'B': 2, "2": 7, 'C': 3, "3": 6, 'D': 4, "4": 5,
          'E': 5, "5": 4, 'F': 6, "6": 3, 'G': 7, "7": 2, 'H': 8, "8": 1}

white_pieces = [["rook", "A1", "white"], ["knight", "B1", "white"], ["bishop", "C1", "white"],
                ["queen", "D1", "white"], ["king", "E1", "white"], ["bishop", "F1", "white"],
                ["knight", "G1", "white"], ["rook", "H1", "white"]]

white_pawns = [["pawn", f"{cols[i]}2", "white"] for i in range(8)]
black_pawns = [["pawn", f"{cols[i]}7", "black"] for i in range(8)]

black_pieces = [["rook", "A8", "black"], ["knight", "B8", "black"], ["bishop", "C8", "black"],
                ["queen", "D8", "black"], ["king", "E8", "black"], ["bishop", "F8", "black"],
                ["knight", "G8", "black"], ["rook", "H8", "black"]]

start = white_pieces + white_pawns + black_pawns + black_pieces

colors = ['black', 'white']
piece_names = ['pawn', 'knight', 'bishop', 'king', 'queen', 'rook']


def load_and_scale(piece, color):
    path = find_piece_image(piece, color)
    image = pygame.image.load(path)

    return pygame.transform.smoothscale(image, (SIZE, SIZE))


dark_square = pygame.Surface((SIZE, SIZE))
dark_square.fill(DARK)
light_square = pygame.Surface((SIZE, SIZE))
light_square.fill(LIGHT)

dark_hover = pygame.Surface((SIZE, SIZE))
dark_hover.fill(DARK_HOVER)
light_hover = pygame.Surface((SIZE, SIZE))
light_hover.fill(DARK_HOVER)

dark_accepted = pygame.Surface((SIZE, SIZE))
dark_accepted.fill(DARK)
pygame.draw.circle(dark_accepted, 'green', (SIZE // 2, SIZE // 2), SIZE // 6)

light_accepted = pygame.Surface((SIZE, SIZE))
light_accepted.fill(LIGHT)
pygame.draw.circle(light_accepted, 'lightgreen', (SIZE // 2, SIZE // 2), SIZE // 6)

piece_surface_library = {f"{c}-{p}": load_and_scale(p, c) for p in piece_names for c in colors}
print(piece_surface_library)
square_surface_library = {'light': light_square, 'light_hover': light_hover,
                          'light_accepted': light_accepted, 'dark': dark_square,
                          'dark_hover': dark_hover, 'dark_accepted': dark_accepted}

# pygame.init()
# window = pygame.display.set_mode((HEIGHT, WIDTH))
# clock = pygame.Clock()
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#     window.fill('white')
#     for index, key in enumerate(square_surface_library):
#         window.blit(square_surface_library[key], (index * SIZE, 0))
#     for index, key in enumerate(piece_surface_library):
#         window.blit(piece_surface_library[key], (index * SIZE, SIZE))
#     clock.tick()
#     pygame.display.update()
