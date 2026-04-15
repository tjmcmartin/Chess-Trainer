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
        self.ui_node = None

    def add_ui_node(self, move, san, color):
        #if there is a ui_node
        if self.ui_node is not None:

            #if the current ui_node has no children
            if self.ui_node.children == []:
                previous = self.ui_node
                self.ui_node = UI_Node(self.surface, previous, move, san, color)
                previous.children.append(self.ui_node)
            #if the current ui_node has children
            else:
                #create a new branch
                print("Branch!")
        #if there isn't already a ui_node
        else:
            #create the head
            self.head = UI_Node(self.surface, None, move, san, color)
            self.ui_node = self.head
        return self.ui_node

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

    def change_position(self, board, ui_node) -> None:
        if self.ui_node == ui_node:
            return
        
        self.ui_node = ui_node
        
        move_diff = ui_node.depth - board.ply()

        if move_diff > 0:
            if move_diff == 1:
                board.push(ui_node.move)
            else:
                print("Big jump forward!")
        elif move_diff < 0:
            if move_diff == -1:
                board.pop()
            else:
                print("Big jump backward!")



    def update(self):
        self.surface.fill("black")

        if self.head is not None:
            self.head.update(self.ui_node)
        
        self.screen.blit(self.surface, (0, 0))
    
class UI_Node():
    def __init__(self, surface, parent, move, text, color):
        self.surface = surface
        self.parent: UI_Node = parent
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
    
    def get_children(self, /, ui_nodes = None):

        if ui_nodes is None:
            ui_nodes = []

        ui_nodes.append(self)
        
        for ui_node in self.children:
            ui_nodes = ui_node.get_children(ui_nodes = ui_nodes)

        return ui_nodes

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