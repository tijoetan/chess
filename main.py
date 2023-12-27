from Data import *
from Board import Board, Player
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Chees")
        self.sprites = pygame.sprite.Group
        self.board = Board()
        self.white = Player(self.board, 'white')
        self.black = Player(self.board, 'black')
        print(self.board.tiles)
        self.clock = pygame.time.Clock()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill('blue')
            self.board.render()
            self.white.get_click()
            self.clock.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()