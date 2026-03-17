import pygame
import chess
from settings import SCREEN_SIZE
from piece import Piece
from tile import Tile
from utils import get_square_from_coords
import globals as G
#--------------------Globals--------------------

board = chess.Board()

#alliases for gropus

#keep track of which piece is highlighted
selected_piece = None

#Create the pygame window
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True

def execute_move(move):
    #deselect the piece
    deselect()

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


for square in chess.SQUARES:
    
    G.tiles[square] = Tile(screen, square)

    piece = board.piece_at(square)
    if piece is not None:
        G.pieces[square] = Piece(screen, piece.piece_type, piece.color, square)

#-------------------Main Loop-------------------
while running:

    #Even handling
    for event in pygame.event.get():

        #Quit the game if they close the game
        if event.type == pygame.QUIT:
            running = False
        #If the clike the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            #Get the mouse position
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

            square = get_square_from_coords(mouse_pos[0], mouse_pos[1])

            if square is not None:

                piece = G.pieces.get(square)

                #if there is no selected piece
                if selected_piece is None:
                    #if there is a piece on the clicked square
                    if piece is not None:
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

                    move = chess.Move(selected_piece.square, square)

                    if move in board.legal_moves:
                        #move
                        pass
                    else:
                        #deselect
                        pass

            
            """
            #loop through all the piece
            for piece in G.pieces.values():

                #if the current piece is getting clicked
                if piece.is_clicked(mouse_pos):

                    #if there is a selected piece
                    if selected_piece is not None:
                        #loop through all the moves
                        for move in get_moves(selected_piece):
                            #if the piece is also a legal move
                            if G.pieces.get(move.to_square) == piece:

                                #delete the old piece
                                piece.kill()

                                #move the selected piece
                                execute_move(move)

                                #the thing that was clicked has been found
                                break

                    #deselect the current piece
                    deselect()
                    
                    #select the new piece
                    selected_piece = piece
                    G.tiles[selected_piece.square].select()

                    for move in get_moves(piece):
                        G.tiles[move.to_square].highlight_move()

                    #the thing that was clicked has been found!
                    break

            #if it wasn't a piece that was clicked
            else:
                #if there is a selected piece
                if selected_piece is not None:
                    #loop through the selected piece's possible moves
                    for move in get_moves(selected_piece):

                        #check if the square was clicked
                        if G.tiles[move.to_square].is_clicked(mouse_pos):
                            
                            #move the selected piece
                            execute_move(move)
                            
                            #the thing that was clicked has been found!
                            break
                    #if a possible move was not clicked
                    else:
                        #deselecte the current piece
                        deselect()
            """
           

    screen.fill("black")

    for tile in G.tiles.values():
        tile.update()

    for piece in G.pieces.values():
        piece.update()

    #display the screen
    pygame.display.flip()

    #cap fps to 60
    clock.tick(60)

#if the loop stops, quite the program
pygame.quit()