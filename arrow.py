import pygame
from pygame import Vector2
from utils import get_x_from_square, get_y_from_square
from settings import ARROW_HEAD_HEIGHT, ARROW_HEAD_WIDTH, ARROW_SHAFT_WIDTH, ARROW_START_OFFSET, ARROW_COLOR

class Arrow(pygame.sprite.Sprite):
    def __init__(self, screen, from_square, to_square, user_created = False):
        super().__init__()
        self.screen = screen
        self.user_created = user_created
        self.from_coords = (get_x_from_square(from_square, True), get_y_from_square(from_square, True))
        self.to_coords = (get_x_from_square(to_square, True), get_y_from_square(to_square, True))
        
        start = Vector2(self.from_coords[0], self.from_coords[1])
        end = Vector2(self.to_coords[0], self.to_coords[1])

        direction = end - start

        u = direction.normalize()
        perp_u = Vector2(-u.y, u.x)
        
        self.head = self.create_head(end, u, perp_u)
        self.shaft = self.create_shaft(start, end, u, perp_u)
        
    def create_head(self, head: Vector2, u: Vector2, perp_u: Vector2) -> tuple[Vector2, Vector2, Vector2]:
        height = u * ARROW_HEAD_HEIGHT
        width_offset = perp_u * ARROW_HEAD_WIDTH
        left_corner = head - height - width_offset
        right_corner = head - height + width_offset
        return (head, left_corner, right_corner)
    
    def create_shaft(self, start: Vector2, end: Vector2, u: Vector2, perp_u: Vector2) -> tuple[Vector2, Vector2, Vector2, Vector2]:
        start_offset = u * ARROW_START_OFFSET
        width_offset = perp_u * ARROW_SHAFT_WIDTH
        head_height = u * ARROW_HEAD_HEIGHT
        
        bottom_left = start + start_offset - width_offset
        bottom_right = start + start_offset + width_offset
        top_left = end - head_height - width_offset
        top_right = end - head_height + width_offset

        return (bottom_right, bottom_left, top_left, top_right)
        
    def update(self):

        pygame.draw.polygon(self.screen, ARROW_COLOR, self.head)
        pygame.draw.polygon(self.screen, ARROW_COLOR, self.shaft)


