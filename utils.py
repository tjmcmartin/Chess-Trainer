import chess
from settings import BOARD_START_X, BOARD_START_Y, TILE_SIZE, BOARD_SIZE
piece_type_map = {
    1: "pawn",
    2: "knight",
    3: "bishop",
    4: "rook",
    5: "queen",
    6: "king"
}

def get_square_from_coords(x: int, y: int):
    """
    gets the square on the chessboard given the pygame coordinates x and y.
    Returns None if the point is outside the board.
    """
    #get the file and rank
    file = (x-BOARD_START_X) // TILE_SIZE
    rank = (y-BOARD_START_Y) // TILE_SIZE

    #check if they are not within bounds
    if not (0 <= file < 8 and 0 <= rank < 8):
        return None

    #return the square
    return chess.square(file, 7-rank)

def get_x_from_square(square, get_center: bool = False) -> int:
    n = 0
    if get_center:
        n = TILE_SIZE/2

    return BOARD_START_X + chess.square_file(square)*TILE_SIZE + n

def get_y_from_square(square, get_center: bool = False) -> int:
    n = 0
    if get_center:
        n = TILE_SIZE/2

    return BOARD_START_Y + (7 - chess.square_rank(square))*TILE_SIZE + n

def is_tile_white(square) -> bool:
    return (chess.square_file(square) + chess.square_rank(square)) %2 == 0

def width_of_space(font) -> int:
    space = font.render(" ", True, (255, 255, 255))
    return space.get_width()

def global_to_right_panel_cords(coordinate):
    new_coordinate = (coordinate[0] - BOARD_START_X - BOARD_SIZE, coordinate[1])
    return new_coordinate