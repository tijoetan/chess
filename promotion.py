import Data
import pygame


class ChoiceBoard():
    def __init__(self, color):
        self.color = color
        self.rect = Data.choice_bkg.get_rect()
        self.rect.center = Data.WIDTH // 2, Data.HEIGHT // 2
        self.order = ['queen', 'rook', 'knight', 'bishop']
        self.font = pygame.font.Font(None)
        self.text = self.font.render('Choose promotion piece', True, 'black')
        self.screen = pygame.display.get_surface()
        # self.font = pygame.font.Font()
        # self.font.render()

    def show(self):
        self.screen.blit(Data.choice_bkg, self.rect)
        for index, piece in enumerate(self.order):
            surface = Data.piece_surface_library[f"{self.color}-{piece}"]
            rect = surface.get_rect(midleft=(Data.SIZE * (2 + index), Data.HEIGHT // 2))
            self.screen.blit(surface, rect)
        self.screen.blit(self.text, self.text.get_rect(midbottom=(Data.WIDTH // 2, Data.HEIGHT // 2 - Data.SIZE // 2)))

    def get_selected(self, pos):
        if abs(Data.HEIGHT // 2 - pos[1]) <= Data.SIZE // 2:
            index = (pos[0] - 2 * Data.SIZE) // Data.SIZE
            if index in range(4):
                return self.order[index]
        return False

    def get_piece(self):
        print('getting piece!')
        pos = pygame.mouse.get_pos()
        piece = self.get_selected(pos)
        return piece if piece else False
