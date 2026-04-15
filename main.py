import pygame
import chess
import chess.pgn
from settings import SCREEN_SIZE, TILE_SIZE, BOARD_START_X, BOARD_START_Y
from piece import Piece
from tile import Tile
from ui import Left_Panel
from utils import get_square_from_coords, get_x_from_square, get_y_from_square, piece_type_map
import globals as G
#------------------------------Globals------------------------------

game = chess.pgn.Game()

game.headers["Event"] = "Opening Trainer"
game.headers["Site"] = "My App"
# game.headers["Date"] = ""
game.headers["Round"] = "-"
game.headers["White"] = "Student"
game.headers["Black"] = "Wizzard Bot"
game.headers["Result"] = "*"

node = game

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

move_tree_ui = Left_Panel(screen)

#-------------------------Function Definitions-------------------------
def is_promotion(move) -> bool:
    #if the move is legal as a promotion
    temp_move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
    if temp_move in board.legal_moves:
        #it is a promotion move
        return True
    
    #it isn't a promotion move
    return False

#Function that sets up promotion variables
def start_promotion(square, color):
    global promotion_pending, promotion_square, promotion_color, promotion_rects
    promotion_pending = True
    promotion_square = square
    promotion_color = color

    promotion_rects = []
    for i in promotion_options:
        rect = pygame.Rect(get_x_from_square(square), get_y_from_square(square) + i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        promotion_rects.append(rect)

def draw_promotion_ui(screen):
    #overlay that darkens the rest of the screen
    overlay = pygame.Surface((TILE_SIZE*8, TILE_SIZE*8), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (BOARD_START_X, BOARD_START_Y))

    #create a square for each promotion option
    for i, piece_type in enumerate(promotion_options):
        rect = promotion_rects[i]
        piece_image = pygame.image.load(f"./assets/{"white" if promotion_color else "black"}_{piece_type_map[piece_type]}.png")
        pygame.draw.rect(screen, (255, 255, 255), promotion_rects[i])
        screen.blit(piece_image, rect.topleft)

def promote(move, piece_type) -> None:

    global node

    #deselect the piece
    deselect()

    #remove the pawn
    pawn = G.pieces[move.from_square]
    pawn.kill()
    del G.pieces[move.from_square]

    #replace it with the user's piece choice
    G.pieces[move.to_square] = Piece(screen, piece_type, board.turn, move.to_square)

    #move the piece on the internal board
    board.push(move)
    node = node.add_variation(move)

def execute_move(move, captured_piece) -> None:

    global node, move_tree_ui

    #deselect the piece
    deselect()

    #check if a piece was captured
    if captured_piece is not None:
        #TODO capture SFX?
        #remove the captured piece
        captured_piece.kill()
        del G.pieces[captured_piece.square]

    #if this isn't the first move
    if board.move_stack:

        #get the last move and undo it's highlights
        last_move = board.peek()
        G.tiles[last_move.from_square].reset_colors()
        G.tiles[last_move.to_square].reset_colors()  

    #highlight the move that was just made
    G.tiles[move.from_square].highlight_last_move()
    G.tiles[move.to_square].highlight_last_move()

    #move the piece in the internal board
    node = node.add_variation(move)
    move_tree_ui.add_ui_node(node, move, board.san(move), board.turn)
    board.push(move)

    #move the piece on the visual board
    G.pieces[move.from_square].update_pos(move.to_square)

def deselect() -> None:

    #get the global variable
    global selected_piece

    if selected_piece is not None:
        #unhighlight all the tiles highlighted as possible moves
        for move in get_moves(selected_piece):
            G.tiles[move.to_square].unhighlight_move()
        
        #deselect the tile the selected piece was on
        G.tiles[selected_piece.square].reset_colors()

    #deselect the piece
    selected_piece = None

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

def get_captured_piece(move):
    if not board.is_capture(move):
        return None

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

    return captured_piece

def change_position(ui_node):

    global node, board

    current_ui_node = move_tree_ui.ui_node
    last_move = current_ui_node.move

    if ui_node == current_ui_node:
        return

    for tile in G.tiles.values():
        tile.reset_colors()

    move_tree_ui.ui_node = ui_node
    node = ui_node.game_node
    board = node.board()
    rebuild_board()

    if board.move_stack:
        last_move = board.peek()
        G.tiles[last_move.to_square].highlight_last_move()
        G.tiles[last_move.from_square].highlight_last_move()


def rebuild_board():

    G.pieces.clear()

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            G.pieces[square] = Piece(screen, piece.piece_type, piece.color, square)


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
        #check for key presses
        elif event.type == pygame.KEYDOWN:
            current_ui_node = move_tree_ui.ui_node
            if current_ui_node is not None:
                if event.key == pygame.K_LEFT:
                    if current_ui_node.parent is not None:
                        change_position(current_ui_node.parent)
                elif event.key == pygame.K_RIGHT:
                    if current_ui_node.children != []:
                        change_position(current_ui_node.children[0])
        #If the clike the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:

            #get the mouse position
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

            if move_tree_ui.head is not None:
                ui_nodes = move_tree_ui.head.get_children()
                for child in ui_nodes:
                    if child.get_clicked(mouse_pos):
                        change_position(child)

            #if we are waiting on a promotion selection from the user
            if promotion_pending and selected_piece is not None and promotion_square is not None:
                #for each of the promotion choices
                for rect, piece_type in zip(promotion_rects, promotion_options):
                    #if the rectangle got clicked
                    if rect.collidepoint(mouse_pos):
                        #promote the right piece
                        move = chess.Move(selected_piece.square, promotion_square, promotion=piece_type)
                        promote(move, piece_type)
                        break
                #if no choice was selected
                else:
                    #deselect the piece
                    deselect()

                #take away the promotion ui
                promotion_pending = False
                promotion_square = None
                promotion_color = None
                promotion_rects = []

            #if were aren't waiting for promotion selection
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

                            #if the move is attempting prmotion
                            if is_promotion(move):
                                #start promotion piece selection process
                                start_promotion(square, board.turn)
                            #if the move is legal
                            elif move in board.legal_moves:
                                
                                #get the captured piece if it exists
                                captured_piece = get_captured_piece(move)

                                #if the moves is castling
                                if board.is_castling(move):
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

    #fill the screen
    screen.fill("black")

    #update the board tiles
    for tile in G.tiles.values():
        tile.update(board)

    #update the visual pieces
    for piece in G.pieces.values():
        piece.update()

    #if we are wiating on promotion, update the promotion ui
    if promotion_pending:
        draw_promotion_ui(screen)

    move_tree_ui.update()

    #display the screen
    pygame.display.flip()

    #cap fps to 60
    clock.tick(60)

#store the data
with open("./openings/test.pgn", "w") as f:
    print(game, file=f)

#if the loop stops, quite the program
pygame.quit()