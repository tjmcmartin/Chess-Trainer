import pygame
import chess
from utils import get_x_from_square, get_y_from_square, is_tile_white
from settings import TILE_SIZE, LIGHT_TILE, DARK_TILE, MOVE_HIGHLIGHT, SELECTED_HIGHLIGHT

class Tile():
    def __init__(self, screen, square):
        self.screen = screen
        self.square = square
        self.rect = pygame.Rect(get_x_from_square(self.square), get_y_from_square(self.square), TILE_SIZE, TILE_SIZE)
        is_white: bool = is_tile_white(self.square)
        self.color = LIGHT_TILE if is_white else DARK_TILE
        self.reset_colors()

    def reset_colors(self):
        self.possible_move = False
        self.selected = False
        self.previous_move = False

    def update(self):

        color = self.color
        if self.possible_move:
            color = MOVE_HIGHLIGHT
        elif self.selected:
            color = SELECTED_HIGHLIGHT
        pygame.draw.rect(self.screen, color, self.rect)

    def select(self):
        self.selected = True

    def highlight_move(self):
        self.possible_move = True

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)