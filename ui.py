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

    def add_node(self, move, san):
        if self.node is not None:
            previous = self.node
            self.node = Node(self.surface, previous, move, san, )
            previous.children.append(self.node)
        else:
            self.head = Node(self.surface, None, move, san)
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

    def update(self):
        self.screen.blit(self.surface, (0, 0))

        if self.head is not None:
            self.head.update()
    
class Node():
    def __init__(self, surface, parent, move, text):
        self.surface = surface
        self.parent: Node = parent
        self.move = move
        self.font = pygame.font.SysFont("default", 30)
        self.text = self.font.render(text + " ", True, (255, 255, 255))
        self.rect = self.text.get_rect()


        if parent is not None:
            self.depth: int = parent.depth + 1
            self.x = parent.x + parent.rect.width
            self.y = parent.y
        else:
            self.depth = 1
            self.x = 0
            self.y = 0

        print(self.rect, self.depth)

        self.children: list[Node] = []

    def update(self):

        self.surface.blit(self.text, (self.x, self.y))

        for node in self.children:
            node.update()
    
    def get_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def get_children(self, /, nodes = None):

        if nodes is None:
            nodes = []

        nodes.append(self)
        
        for node in self.children:
            nodes = node.get_children(nodes = nodes)

        return nodes
