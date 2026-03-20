import pygame
from settings import BOARD_START_X, SCREEN_SIZE

class Left_Panel():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont('default', 30)
        self.text = ""
        self.rect = pygame.Rect(0, 0, BOARD_START_X, SCREEN_SIZE[1])
        self.surface = pygame.Surface(self.rect.size)
        self.head = None
        self.node = None

    def add_node(self, move):
        if self.node is not None:
            previous = self.node
            self.node = Node(previous, move, previous.depth+1)
            previous.children.append(self.node)
        else:
            self.head = Node(None, move, 1)
            self.node = self.head
        return self.node

    def update_text(self, san):
        #split the text into lines and get the last line
        lines = self.text.split("\n")
        last_line = lines[-1] if lines else ""


        line_width, _ = self.font.size(last_line + " " + san)
        sep = " "

        if line_width > self.rect.width:
            sep = "\n"

        self.text = sep.join([self.text, san])

        text = self.font.render(self.text, True, (255, 255, 255))
        self.surface.blit(text, (0, 0))

    def update(self):
        self.screen.blit(self.surface, (0, 0))
    
class Node():
    def __init__(self, parent, move, depth: int):
        self.parent: Node = parent
        self.move = move
        self.depth: int = depth
        self.children: list[Node] = []