import pygame

SCREEN_SIZE: tuple[int, int] = (1280, 720)

#Tile & board settings
TILE_SIZE: int = 75
BOARD_SIZE = TILE_SIZE*8
BOARD_START_X: int = (SCREEN_SIZE[0] - BOARD_SIZE) // 2 
BOARD_START_Y: int = 0 #(SCREEN_SIZE[1] - TILE_SIZE*8) 

#Training mode settings
RESPONSE_DELAY = 1000 #this is in ms

#Arrow settings
ARROW_HEAD_HEIGHT = 25
ARROW_HEAD_WIDTH = 25
ARROW_SHAFT_WIDTH = 10
ARROW_START_OFFSET = TILE_SIZE/2

#Move list settings
LEFT_PANEL_MARGIN = 0
INDENT_SIZE = 10
BRANCH_INDENT_SIZE = 20
NEW_LINE_SIZE = 20

#Colors
LIGHT_TILE = (240, 240, 240)
DARK_TILE  = (31, 95, 173)
SELECTED_HIGHLIGHT   = (255, 191, 0) #Tile that the user selects
MOVE_HIGHLIGHT  = (255, 235, 120) #Tile that highlights the previous move
# ARROW_COLOR = (183, 194, 74)
ARROW_COLOR = (163, 179, 77)

#Possible move highlight shapes
MOVE_DOT = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
pygame.draw.circle(MOVE_DOT, (0, 0, 0, 120), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//5)
MOVE_CIRCLE = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
pygame.draw.circle(MOVE_CIRCLE, (0, 0, 0, 120), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2, width=10)