from Data import *
from Board import Board, Piece
from Player import Player
from promotion import ChoiceBoard
import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.board = Board()
        self.white = Player(self.board, 'white')
        self.black = Player(self.board, 'black')
        # print(self.board.tiles)
        self.clock = pygame.time.Clock()
        self.has_piece = False
        self.player = self.white

        self.show_choice = False
        self.choice_boards = {'white': ChoiceBoard('white'), 'black': ChoiceBoard('black')}

        self.player.update_moves()

    def switch(self, player):
        return self.white if player == self.black else self.black

    def render_board(self):
        for tile in self.board.tiles.values():
            square = tile[0]
            piece = tile[1]
            self.screen.blit(square_surface_library[square.surf_source], square.rect)
            if piece is not None:
                self.screen.blit(piece_surface_library[f"{piece.color}-{piece.type}"], piece.rect)
        moving_piece = self.player.held_piece
        if moving_piece is not None:
            self.screen.blit(piece_surface_library[f"{moving_piece.color}-{moving_piece.type}"], moving_piece.rect)
        if self.show_choice:
            self.choice_boards[self.player.color].show()

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.show_choice:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.has_piece:
                            try:
                                x = self.player.put_down()
                            except TypeError:
                                self.show_choice = True
                                break

                            self.has_piece = False
                            if x:
                                self.player = self.switch(self.player)
                                self.player.update_moves()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_choice:
                        piece = self.choice_boards[self.player.color].get_piece()
                        if piece:
                            current_piece = self.player.held_piece
                            current_piece: Piece or None
                            self.board.tiles[current_piece.position][1] = Piece(piece, current_piece.position,
                                                           current_piece.color, current_piece.moves + 1)
                            self.has_piece = False
                            self.player.held_piece = None
                            self.player = self.switch(self.player)
                            self.player.update_moves()
                            self.show_choice = False
                    else:
                        self.has_piece = True if self.player.pickup() is not None else False

            self.screen.fill('blue')
            self.player.color_tiles()
            self.render_board()
            if self.has_piece and not self.show_choice:
                self.player.move_lifted()
            self.clock.tick(60)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
