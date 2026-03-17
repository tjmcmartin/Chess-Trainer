import pygame
import chess
from settings import BOARD_START_X, BOARD_START_Y, TILE_SIZE
from utils import piece_type_map, get_x_from_square, get_y_from_square
import globals as G

class Piece(pygame.sprite.Sprite):
    def __init__(self, screen, type, color, square) -> None:
        super().__init__()
        self.screen = screen
        self.square = square
        self.color = color
        self.image = pygame.image.load(f"./assets/{"white" if color else "black"}_{piece_type_map[type]}.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (get_x_from_square(self.square), get_y_from_square(self.square))

    def update(self) -> None:
        self.screen.blit(self.image, self.rect)

    def update_pos(self, square) -> None:
        
        #update the piece's position
        del G.pieces[self.square]
        G.pieces[square] = self
        
        #update the piece's variables
        self.square = square
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)

        #move the rectangle (and with it the piece)
        self.rect.topleft = (BOARD_START_X + col*TILE_SIZE,
                             BOARD_START_Y + row*TILE_SIZE)
    
    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)