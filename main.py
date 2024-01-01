from Data import *
from Board import Board
from Player import Player
import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.sprites = pygame.sprite.Group
        self.board = Board()
        self.white = Player(self.board, 'white')
        self.black = Player(self.board, 'black')
        # print(self.board.tiles)
        self.clock = pygame.time.Clock()
        self.show_piece = False

        self.player = self.white

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

    def run(self):
        self.player.update_moves()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.show_piece:
                        x = self.player.put_down()
                        self.show_piece = False
                        if x:
                            self.player = self.switch(self.player)
                            self.player.update_moves()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.show_piece = True if self.player.pickup() is not None else False

            self.screen.fill('blue')
            self.player.color_tiles()
            self.render_board()
            if self.show_piece:
                self.player.move_lifted()
            self.clock.tick(60)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
