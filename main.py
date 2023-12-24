from Data import *
from Board import Board
import pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chees")
sprites = pygame.sprite.Group
board = Board()
print(board.tiles)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill('blue')
    board.render()
    clock.tick(60)
    pygame.display.update()