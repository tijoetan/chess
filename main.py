from Data import *
from Board import Board, Piece
from Player import Player
from Menus import ChoiceBoard, GameOver
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

        self.over = False
        self.over_screen = None
        # print(self.board.tiles)
        self.clock = pygame.time.Clock()
        self.has_piece = False
        self.player = self.white

        self.show_choice = False
        self.choice_boards = {'white': ChoiceBoard('white'), 'black': ChoiceBoard('black')}

        self.player.update_moves()


    def end(self, type):
        if type == 1:
            self.over_screen = GameOver('checkmate')
            self.over = True
        elif type == 2:
            self.over_screen = GameOver('stalemate')
            self.over = True


    def switch_update(self):
        self.player = self.white if self.player == self.black else self.black
        moves = self.player.update_moves()
        if moves is not None:
            self.end(moves)


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
        if self.over:
            text = self.over_screen.text
            self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

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
                            except KeyError:
                                self.show_choice = True
                                break

                            self.has_piece = False
                            if x:
                                self.switch_update()
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
                            self.switch_update()
                            self.show_choice = False
                    else:
                        self.has_piece = True if self.player.pickup() is not None else False

            #self.screen.fill('')
            self.player.color_tiles()
            self.render_board()
            if self.has_piece and not self.show_choice:
                self.player.move_lifted()
            self.clock.tick(60)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    if not game.over:
        game.run()
    else:
        game.render_board()
