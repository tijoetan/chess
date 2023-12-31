import pygame
from pygame import gfxdraw
from files import find_piece_image

print(pygame.color.THECOLORS['lightgreen'])
WIDTH = 8 * 90
HEIGHT = WIDTH
# LIGHT = pygame.Color(240, 217, 181)
# DARK = pygame.Color(181, 136, 99)
LIGHT = pygame.Color(230, 220, 210)
DARK = pygame.Color(160, 70, 75)

DARK_HOVER = DARK.lerp('blue', 0.3)
LIGHT_HOVER = LIGHT.lerp('blue', 0.3)

DARK_ACCEPT = DARK.lerp('green', 0.7)
LIGHT_ACCEPT = LIGHT.lerp('green',0.7)

SIZE = int(WIDTH // 8)
text_size = SIZE // 2

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


def circle(surface, x, y, radius, color):
    # pygame.draw.circle(surface, color, (x,y), radius)
    gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)


dark_square = pygame.Surface((SIZE, SIZE))
dark_square.fill(DARK)

light_square = pygame.Surface((SIZE, SIZE))
light_square.fill(LIGHT)

dark_hover = pygame.Surface((SIZE, SIZE))
dark_hover.fill(DARK_HOVER)
light_hover = pygame.Surface((SIZE, SIZE))
light_hover.fill(LIGHT_HOVER)

dark_accepted = pygame.Surface((SIZE, SIZE))
dark_accepted.fill(DARK)
circle(dark_accepted, SIZE // 2, SIZE // 2, SIZE // 6, DARK_ACCEPT)

light_accepted = pygame.Surface((SIZE, SIZE))
light_accepted.fill(LIGHT)
circle(light_accepted, SIZE // 2, SIZE // 2, SIZE // 6, LIGHT_ACCEPT)

dark_capture = pygame.Surface((SIZE, SIZE))
dark_capture.fill('green')
circle(dark_capture, SIZE // 2, SIZE // 2, SIZE // 1.7, DARK)

light_capture = pygame.Surface((SIZE, SIZE))
light_capture.fill('lightgreen')
circle(light_capture, SIZE // 2, SIZE // 2, SIZE // 1.7, LIGHT)

choice_bkg = pygame.Surface((SIZE * 4, SIZE))
choice_bkg.fill('gray')

piece_surface_library = {f"{c}-{p}": load_and_scale(p, c) for p in piece_names for c in colors}
print(piece_surface_library)
square_surface_library = {'light': light_square, 'light_hover': light_hover,
                          'light_accepted': light_accepted, 'dark': dark_square,
                          'dark_hover': dark_hover, 'dark_accepted': dark_accepted,
                          'dark_capture': dark_capture, 'light_capture': light_capture}

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
#     window.blit(choice_bkg, (WIDTH//2, HEIGHT//2))
#     clock.tick()
#     pygame.display.update()
