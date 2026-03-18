import pygame
import chess
from settings import SCREEN_SIZE, TILE_SIZE, BOARD_START_X, BOARD_START_Y
from piece import Piece
from tile import Tile
from utils import get_square_from_coords, get_x_from_square, get_y_from_square, piece_type_map
import globals as G
#------------------------------Globals------------------------------

board = chess.Board()

promotion_pending = False
promotion_square = None
promotion_color = None
promotion_rects = []
promotion_options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]

#keep track of which piece is highlighted
selected_piece = None

#Create the pygame window
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True

#-------------------------Function Definitions-------------------------
def is_promotion(move) -> bool:
    piece = G.pieces.get(move.from_square)
    if piece is not None and piece.type == chess.PAWN and (
        (piece.color == chess.WHITE and chess.square_rank(move.to_square) == 7) or
        (piece.color == chess.BLACK and chess.square_rank(move.to_square) == 0)):
        return True
    
    return False

def start_promotion(square, color):
    global promotion_pending, promotion_square, promotion_color, promotion_rects
    promotion_pending = True
    promotion_square = square
    promotion_color = color

    promotion_rects = []
    for i, piece_type in enumerate(promotion_options):
        rect = pygame.Rect(get_x_from_square(square) + i*TILE_SIZE, get_y_from_square(square), TILE_SIZE, TILE_SIZE)
        promotion_rects.append(rect)

def draw_promotion_ui(screen):
    overlay = pygame.Surface((TILE_SIZE*8, TILE_SIZE*8), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (BOARD_START_X, BOARD_START_Y))

    for i, piece_type in enumerate(promotion_options):
        rect = promotion_rects[i]
        piece_image = pygame.image.load(f"./assets/{"white" if promotion_color else "black"}_{piece_type_map[piece_type]}.png")
        screen.blit(piece_image, rect.topleft)


def choose_promotion(rects, options):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, piece_type in zip(rects, options):
                    if rect.collidepoint(mouse_pos):
                        return piece_type
                    # else:
                    #     return None

def promote(move, piece_type) -> None:
    deselect()

    pawn = G.pieces[move.from_square]
    pawn.kill()
    del G.pieces[move.from_square]

    G.pieces[move.to_square] = Piece(screen, piece_type, board.turn, move.to_square)

    board.push(move)

def execute_move(move, captured_piece):
    #deselect the piece
    deselect()

    #check if a piece was captured
    if captured_piece is not None:
        #TODO capture SFX?
        #remove the captured piece
        captured_piece.kill()
        del G.pieces[captured_piece.square]

    #move the piece in the internal board
    board.push(move)

    #move the piece on the visual board
    G.pieces[move.from_square].update_pos(move.to_square)

def deselect() -> None:
    if selected_piece is not None:
        #unhighlight all the tiles highlighted as possible moves
        for move in get_moves(selected_piece):
            G.tiles[move.to_square].reset_colors()
        
        #deselect the tile the selected piece was on
        G.tiles[selected_piece.square].reset_colors()

def select(piece) -> None:

    global selected_piece

    #selecte the piece
    selected_piece = piece

    G.tiles[selected_piece.square].select()

    for move in get_moves(selected_piece):
        G.tiles[move.to_square].highlight_move()

def get_moves(piece) -> list:
    moves = []
    for move in board.legal_moves:
        if move.from_square == piece.square:
            moves.append(move)

    return moves

#set up the board
#for each square on the board
for square in chess.SQUARES:
    
    #create a visual tile for it
    G.tiles[square] = Tile(screen, square)

    #get the piece on the square
    piece = board.piece_at(square)

    #if it exists
    if piece is not None:
        #create a visual piece there
        G.pieces[square] = Piece(screen, piece.piece_type, piece.color, square)

#-----------------------------Main Loop-----------------------------
while running:

    #Even handling
    for event in pygame.event.get():

        #Quit the game if they close the game
        if event.type == pygame.QUIT:
            running = False
        #If the clike the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            #get the mouse position
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

            if promotion_pending:
                for rect, piece_type in zip(promotion_rects, promotion_options):
                    if rect.collidepoint(mouse_pos):
                        move = chess.Move(selected_piece.square, promotion_square, promotion=piece_type)
                        promote(move, piece_type)

                        promotion_pending = False
                        promotion_square = None
                        promotion_color = None
                        promotion_rects = []

            else:
                #get the square that got clicked
                square = get_square_from_coords(mouse_pos[0], mouse_pos[1])

                #if the square exists
                if square is not None:

                    #get the peice that's on the square (if any)
                    piece = G.pieces.get(square)

                    #if there is no selected piece
                    if selected_piece is None:
                        #if there is a piece on the clicked square
                        if piece is not None and piece.color == board.turn:
                            #select the piece
                            select(piece)

                    #if there is a selected piece
                    else:
                        #if the piece being clicked is a friendly piece
                        if piece is not None and piece.color == board.turn:
                            #deselect the old piece
                            deselect()

                            #selecte the new piece
                            select(piece)
                        #if the piece is not friendly or there is no piece
                        else:
                            #create a move from the selected piece to the clicked square
                            move = chess.Move(selected_piece.square, square)

                            if is_promotion(move):
                                start_promotion(square, board.turn)
                            #if the move is legal
                            elif move in board.legal_moves:
                                
                                #default value if it isn't a capture
                                captured_piece = None

                                #if the moves is a capture
                                if board.is_capture(move):

                                    #if the move is en passent
                                    if board.is_en_passant(move):
                                        #if it is white's turn
                                        if board.turn:
                                            #get the square one below where the pawn moved
                                            pawn_square = move.to_square -8
                                        #if it is black's turn
                                        else:
                                            #get the square one above where the pawn moved
                                            pawn_square = move.to_square + 8
                                        
                                        #set that square as the captured peice
                                        captured_piece = G.pieces.get(pawn_square)

                                    #if the move is just a normal capture
                                    else:
                                        captured_piece = G.pieces.get(move.to_square)

                                #if the moves is castling
                                elif board.is_castling(move):
                                    #check if the king castled queenside
                                    if chess.square_file(move.to_square) == 2:
                                        rook_from = move.to_square - 2
                                        rook_to = move.to_square + 1
                                    #if the king caslted kingside
                                    else:
                                        rook_from = move.to_square + 1
                                        rook_to = move.to_square - 1
                                    
                                    #if the rook is there, move it
                                    rook = G.pieces.get(rook_from)
                                    if rook is not None:
                                        rook.update_pos(rook_to)
                                





                                #execute the move
                                execute_move(move, captured_piece)
                            #if the move is not legal
                            else:
                                #deselecte the selected piece
                                deselect()

    screen.fill("black")

    for tile in G.tiles.values():
        tile.update()

    for piece in G.pieces.values():
        piece.update()

    if promotion_pending:
        draw_promotion_ui(screen)

    #display the screen
    pygame.display.flip()

    #cap fps to 60
    clock.tick(60)

#if the loop stops, quite the program
pygame.quit()