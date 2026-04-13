import pygame
import chess
from settings import BOARD_START_X, SCREEN_SIZE, LEFT_PANEL_MARGIN
from utils import width_of_space

class Left_Panel():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont('default', 30)
        self.text = ""
        self.rect = pygame.Rect(0, 0, BOARD_START_X, SCREEN_SIZE[1])
        self.surface = pygame.Surface(self.rect.size)
        self.head = None
        self.node = None

    def add_node(self, move, san, color):
        if self.node is not None:
            previous = self.node
            self.node = Node(self.surface, previous, move, san, color)
            previous.children.append(self.node)
        else:
            self.head = Node(self.surface, None, move, san, color)
            self.node = self.head
        return self.node

    # def update_text(self, san):
    #     #split the text into lines and get the last line
    #     lines = self.text.split("\n")
    #     last_line = lines[-1] if lines else ""


    #     line_width, _ = self.font.size(last_line + " " + san)
    #     sep = " "

    #     if line_width > self.rect.width:
    #         sep = "\n"

    #     self.text = sep.join([self.text, san])

    #     text = self.font.render(self.text, True, (255, 255, 255))
    #     self.surface.blit(text, (0, 0))

    def change_position(self, node) -> None:
        if self.node == node:
            return
        
        self.node = node
        print("change position!")

    def update(self):
        self.surface.fill("black")

        if self.head is not None:
            self.head.update(self.node)
        
        self.screen.blit(self.surface, (0, 0))
    
class Node():
    def __init__(self, surface, parent, move, text, color):
        self.surface = surface
        self.parent: Node = parent
        self.move = move
        self.color = color
        self.depth = 1
        if parent is not None:
            self.depth: int = parent.depth + 1
    
        self.font = pygame.font.SysFont("default", 30)
        if self.color == chess.WHITE:
            text = str( (self.depth+1) // 2 ) + ". " + text

        self.text = self.font.render(text + " ", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        
        self.x, self.y = self.create_coords(self.parent)
        
        self.rect.topleft = (self.x, self.y)

        self.children: list[Node] = []

    def update(self, current_node):
        if self == current_node:
            offset = width_of_space(self.font)/2
            pygame.draw.rect(self.surface, (70, 90, 130), pygame.Rect((self.x - offset, self.y), self.rect.size))
        self.surface.blit(self.text, (self.x, self.y))

        for node in self.children:
            node.update(current_node)
    
    def get_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def get_children(self, /, nodes = None):

        if nodes is None:
            nodes = []

        nodes.append(self)
        
        for node in self.children:
            nodes = node.get_children(nodes = nodes)

        return nodes

    def create_coords(self, parent) -> tuple[int, int]:

        if parent is None:
            return LEFT_PANEL_MARGIN, 0

        x = parent.x
        y = parent.y

        temp_x = x + parent.text.get_width()

        #check if wrapping is needed
        if temp_x + self.text.get_width() > self.surface.get_width() + LEFT_PANEL_MARGIN:
            #put it on a new line
            y += 20
            x = LEFT_PANEL_MARGIN
        #if wrapping is not needed
        else:
            #shift the x over by the parent's width
            x = temp_x

        return x, y