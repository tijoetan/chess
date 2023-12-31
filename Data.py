from pygame import Color

WIDTH = 8 * 60
HEIGHT = WIDTH
LIGHT = Color(240, 217, 181)
DARK = Color(181, 136, 99)
SIZE = WIDTH / 8

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
