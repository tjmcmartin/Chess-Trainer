import pygame
from utils import get_x_from_square, get_y_from_square, is_tile_white
from settings import TILE_SIZE, LIGHT_TILE, DARK_TILE, MOVE_DOT, MOVE_CIRCLE, SELECTED_HIGHLIGHT, MOVE_HIGHLIGHT

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
        self.last_move_highlight = False

    def update(self, board):

        color = self.color
        if self.last_move_highlight:
            color = MOVE_HIGHLIGHT
        elif self.selected:
            color = SELECTED_HIGHLIGHT
        pygame.draw.rect(self.screen, color, self.rect)
        if self.possible_move:
            thing_to_draw = MOVE_DOT
            if board.piece_at(self.square):
                thing_to_draw = MOVE_CIRCLE
            self.screen.blit(thing_to_draw, self.rect.topleft)

    def select(self):
        self.selected = True

    def highlight_move(self):
        self.possible_move = True

    def unhighlight_move(self):
        self.possible_move = False

    def highlight_last_move(self):
        self.last_move_highlight = True

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)