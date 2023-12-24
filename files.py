import os

pieces = {}
for root, dirs, files in os.walk("piece sprites"):
    for name in files:
        pieces[name.split('.')[0]] = os.path.join(root, name)

def find_piece_image(piece: str, color: str) -> str:
    search_string = f"{color}-{piece}"
    return pieces[search_string]


