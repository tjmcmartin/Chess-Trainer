import chess
from settings import BOARD_START_X, BOARD_START_Y, TILE_SIZE
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

def get_x_from_square(square) -> int:
    return BOARD_START_X + chess.square_file(square)*TILE_SIZE

def get_y_from_square(square) -> int:
    return BOARD_START_Y + (7 - chess.square_rank(square))*TILE_SIZE

def is_tile_white(square) -> bool:
    return (chess.square_file(square) + chess.square_rank(square)) %2 == 0