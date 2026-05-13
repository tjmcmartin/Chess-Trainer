import pygame
import chess
import os
import globals as G
from settings import BOARD_START_X, SCREEN_SIZE, LEFT_PANEL_MARGIN, NEW_LINE_SIZE, BRANCH_INDENT_SIZE, BOARD_SIZE
from utils import width_of_space, global_to_right_panel_cords

class Left_Panel():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont('default', 30)
        self.rect = pygame.Rect(0, 0, BOARD_START_X, SCREEN_SIZE[1])
        self.surface = pygame.Surface(self.rect.size)
        self.head = None
        self.ui_node = None

    def add_ui_node(self, node, move, san, color):
        #if there is a ui_node
        if self.ui_node is not None:

            #if the current ui_node has no children
            if self.ui_node.children == []:
                #create a ui node normally
                new_ui_node = UI_Node(self.surface, self.ui_node, move, san, color, node)
            #if the ui node already has children
            else:
                #create a new branch
                new_ui_node = UI_Node(self.surface, self.ui_node, move, san, color, node, new_branch=True)
            self.ui_node.children.append(new_ui_node)
            self.ui_node = new_ui_node
        #if there isn't already a ui_node
        else:
            #create the head
            self.head = UI_Node(self.surface, None, move, san, color, node)
            self.ui_node = self.head

    def update(self):
        self.surface.fill("black")

        if self.head is not None:
            self.head.update(self.ui_node)
        
        self.screen.blit(self.surface, (0, 0))
    
class UI_Node():
    def __init__(self, surface, parent, move, text, color, node, /, new_branch=False):
        self.game_node = node
        self.surface = surface
        self.parent: UI_Node = parent
        self.move = move
        self.color = color
        self.depth = 1
        if parent is not None:
            self.depth: int = parent.depth + 1
    
        self.font = pygame.font.SysFont("default", 30)
        if self.color == chess.WHITE:
            text = str( (self.depth+1) // 2 ) + "." + text
        elif new_branch and self.color == chess.BLACK:
            text = str(self.depth//2) + "..." + text

        self.text = self.font.render(text + " ", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        
        self.x, self.y = self.create_coords(self.parent, new_branch)
        
        self.rect.topleft = (self.x, self.y)

        self.children: list[UI_Node] = []

    def update(self, current_ui_node):
        if self == current_ui_node:
            offset = width_of_space(self.font)/2
            pygame.draw.rect(self.surface, (70, 90, 130), pygame.Rect((self.x - offset, self.y), self.rect.size))
        self.surface.blit(self.text, (self.x, self.y))

        for ui_node in self.children:
            ui_node.update(current_ui_node)
    
    def get_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
    
    def get_branch_depth(self):
        depth = 0

        if self.parent is None:
            return 0

        if self.parent.children.__len__() > 1:
            depth += 1

        new_depth = self.parent.get_branch_depth()

        return depth + new_depth
    
    def get_children(self, /, ui_nodes = None):

        if ui_nodes is None:
            ui_nodes = []

        ui_nodes.append(self)
        
        for ui_node in self.children:
            ui_nodes = ui_node.get_children(ui_nodes = ui_nodes)

        return ui_nodes
    
    def get_branch_height(self) -> int:

        if self.children == []:
            return self.y
        else:
            return self.children[-1].get_branch_height()

    def create_coords(self, parent, new_branch=False) -> tuple[int, int]:

        #if there is no parent
        if parent is None:
            #return the coordinates of where the first node should go
            return LEFT_PANEL_MARGIN, 0

        #temporarily set cordinates to the parent's values
        x = parent.x
        y = parent.y

        #if this node is starting a new branch
        if new_branch:
            #set the x indent depending on the depth
            x = LEFT_PANEL_MARGIN + BRANCH_INDENT_SIZE * (1 + self.parent.get_branch_depth())
            #set the y value below all branches from the same parent
            y = parent.get_branch_height() + NEW_LINE_SIZE
        #if the node is not a new branch
        else:
            #create a test x value
            temp_x = x + parent.text.get_width()

            #check if wrapping is needed
            if temp_x + self.text.get_width() > self.surface.get_width() + LEFT_PANEL_MARGIN:
                #put it on a new line
                y += NEW_LINE_SIZE
                x = LEFT_PANEL_MARGIN
            #if wrapping is not needed
            else:
                #shift the x over by the parent's width
                x = temp_x

        return x, y
    
class Right_Panel():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("default", 30)
        x = BOARD_START_X + BOARD_SIZE
        self.rect = pygame.Rect(x, 0, SCREEN_SIZE[0] - x, SCREEN_SIZE[1])
        self.screen_x_offset = x
        self.surface = pygame.Surface(self.rect.size)
        self.openings = []

        y = 0
        for path in (G.project_root / "openings").iterdir():
            file_name = path.name
            self.openings.append(Opening_Button(self.surface, path, file_name, 0, y))
            y += 30

    def update(self):
        self.surface.fill("black")

        for button in self.openings:
            button.update()

        self.screen.blit(self.surface, self.rect.topleft)     

class Button():
    def __init__(self, surface, path, file_name, x, y):
        self.surface = surface
        self.file = path
        self.font = pygame.font.SysFont("default", 30)
        self.text = self.font.render(file_name, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.rect = self.text_rect.inflate(40, 20)
        self.rect.topleft = (x, y)
        self.text_rect.center = self.rect.center

    def update(self):
        pygame.draw.rect(self.surface, (70, 90, 130), self.rect, border_radius=20)
        self.surface.blit(self.text, self.text_rect)
    
    def get_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(global_to_right_panel_cords(mouse_pos))

class Opening_Button(Button):
    def __init__(self, surface, path, file_name, x, y):
        super().__init__(surface, path, file_name, x, y)
        self.variations = []
        if self.file.is_dir():
            for file_path in self.file.iterdir():
                file_name = file_path.name
                print(f"created variation button for file {file_name}")
                self.variations.append(Variation_Button(self.surface, file_path, file_name, x, y+200))


class Variation_Button(Button):
    def __init__(self, surface, path, file_name, x, y):
        super().__init__(surface, path, file_name, x, y)