# Celtic basic AI
# Group I:
#
#  Update:
#   - Bug Fixes; rotates and shfts appropriate weights
#   - Players cannot place a tile in a non legal space
#   - Added white row, rules, tile
#   - Weights now rotate with the tile in both classes
#   - Space is now used to rotate a tile and escape key to close game
#
#  Notes:
#  - Check to see if weights are correctly assigned, may be bugged
#  - Currently there is no check if a player selects more than one tile
#  - If blue player 2 selects a white piece the tile on the baord is blue when should be white


import pygame
from pygame.locals import *
from Celtic_classes import vector2, TileBoard, TilePlayer, rotateButton

SCREEN_width = 1024
SCREEN_height = 752
TILESIZE_width = 70
TILESIZE_height = 70  # Used to be 68

player1_color = (255, 0, 0)     # RED
player2_color = (0, 0, 255)     # BLUE
selected_color = (255, 255, 0)  # YELLOW
idle_color = (0, 137, 68)       # GREEN
legal_color = (255,118,49)      # ORANGE

# MAIN GAME SEGMENT       #######################################################

# Creates rotate button
button = pygame.image.load("imgs/rotate_button.png")
button = pygame.transform.scale(button, (int(120), int(120)))
rotate = rotateButton(button, vector2(30, 500))

# Title and rules
p1_wins = pygame.image.load("imgs/player1_win.png")
title = pygame.image.load("imgs/celtic_name.png")
pieces_rules = pygame.image.load("imgs/pieces_rules.png")
scores_notes = pygame.image.load("imgs/scores_notes.png")

# Creates 5 X 5 board setup
col = 0
row = 0
boardArray = []
for i in range(25):
    if col < 5:
        newTile = TileBoard(vector2(200 + (col * TILESIZE_width), 104 + (row * TILESIZE_height)),
                            selected_color, col + 1, row + 1)
        # Applies an identity to the tile, ei. "image, set weights, orientation"
        if i == 12:
            newTile.tile_setup(04, 3, 0)
            newTile.active = True
            newTile.legal_move = True
        boardArray.append(newTile)
        col += 1
    else:
        col = 0
        row += 1
        newTile = TileBoard(vector2(200 + (col * TILESIZE_width), 104 + (row * TILESIZE_height)),
                            selected_color, col + 1, row + 1)
        boardArray.append(newTile)
        col += 1

# Creates Player 1's 2 X 5 board setup
col = 0
row = 0
tileCount = 0
tileId = 00
player1Board = []
for i in range(10):
    if col < 2:
        newTile = TilePlayer(vector2(20 + (col * TILESIZE_width), 104 + (row * TILESIZE_height + 4)), player1_color, 1)
        player1Board.append(newTile)
        col += 1
    else:
        col = 0
        row += 1
        newTile = TilePlayer(vector2(20 + (col * TILESIZE_width), 104 + (row * TILESIZE_height + 4)), player1_color, 1)
        player1Board.append(newTile)
        col += 1

# Applies an identity to the tile, ei. "image, set weights, orientation"
    # Ensures tiles are only made in
    if tileCount < 2:
        newTile.tile_setup(tileId)
        tileCount += 1
    else:
        tileId += 1
        tileCount = 0
        newTile.tile_setup(tileId)
        tileCount += 1

#   Creates Player 2's 2 X 5 board setup
col = 0
row = 0
tileCount = 0
tileId = 00
player2Board = []
for i in range(10):
    if col < 2:
        newTile = TilePlayer(vector2(574 + (col * TILESIZE_width), 104 + (row * TILESIZE_height)), player2_color, 2)
        player2Board.append(newTile)
        col += 1
    else:
        col = 0
        row += 1
        newTile = TilePlayer(vector2(574 + (col * TILESIZE_width), 104 + (row * TILESIZE_height)), player2_color, 2)
        player2Board.append(newTile)
        col += 1
# Applies an identity to the tile, ei. "image, set weights, orientation"
    # Ensures tiles are only made in
    if tileCount < 2:
        newTile.tile_setup(tileId)
        tileCount += 1
    else:
        tileId += 1
        tileCount = 0
        newTile.tile_setup(tileId)
        tileCount += 1


# Creates neutral board
col = 0
row = 0
tileCount = 0
tileId = 00
whiteBoard = []
for i in range(5):
    newTile = TilePlayer(vector2(200 + (col * TILESIZE_width), 484 + (row * TILESIZE_height)), legal_color, 3)
    whiteBoard.append(newTile)
    col += 1
# Applies an identity to the tile, ei. "image, set weights, orientation"
    # Ensures tiles are singular
    if tileCount < 1:
        newTile.tile_setup(tileId)
        tileCount += 1
    else:
        tileId += 1
        tileCount = 0
        newTile.tile_setup(tileId)
        tileCount += 1

#   End of board setup    #############

screen = pygame.display.set_mode((SCREEN_width, SCREEN_height))
pygame.display.set_caption('Celtic!: Game Theory Edition')

# get mouse
mouse_pos = pygame.mouse.get_pos()

# Bool var. to ensure only one tile is selected at a time
player1select = False
player2select = False

# List with board_id of selected tiles
selected_p1 = []
selected_p2 = []
selected_white = []

# Indicates whose turn it is
turn_player1 = True

print("Greetings Dr. Wylie,\n we've been expecting you.\n\nRotate your tiles by clicking"
      "the tile and pressing the space bar or the rotate button\n")
print("Player 1: Make your move")

select_tile_p1 = False
select_tile_p2 = False

undoTile = False

running = True
while running:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Rotating tile from space bar!")
                rotate.active = True
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_u:
                undoTile = True
        elif event.type == MOUSEBUTTONDOWN:
            # If the mouse is clicked within the tile's space, set flag
            mouse_pos = pygame.mouse.get_pos()

            # Checks player1Board to see which tile player selects
            for tile in player1Board:
                if tile.rect.collidepoint(mouse_pos) and turn_player1:
                    # print ("Mouse was clicked inside Player 1's board!")
                    tile.mouse_click = True
                    # Adds tile object to Selected, a list that holds selected tiles
                    selected_p1.append(tile)

            # Checks player2Board to see which tile player selects
            for tile in player2Board:
                if tile.rect.collidepoint(mouse_pos) and turn_player1 == False:
                    # print ("Mouse was clicked inside Player 2's board!")
                    tile.mouse_click = True
                    # Adds tile object to Selected, a list that holds selected tiles
                    selected_p2.append(tile)

            # Checks whiteBoardBoard to see which tile player selects
            for tile in whiteBoard:
                if tile.rect.collidepoint(mouse_pos):
                    # print ("Mouse was clicked inside Player 2's board!")
                    tile.mouse_click = True
                    # Adds tile object to Selected, a list that holds selected tiles
                    if turn_player1:
                        selected_p1.append(tile)
                    else:
                        selected_p2.append(tile)

            # Checks if rotate button is selected
            if rotate.rect.collidepoint(mouse_pos):
                print("Rotating tile!")
                # Set to active, now when tile is updating and is selected, call rotate
                rotate.active = True

            for i in range(25):
                if boardArray[i].rect.collidepoint(mouse_pos):
                    # print ("Mouse was clicked inside main board!")
                    if turn_player1 and boardArray[i].legal_move:
                        # Yes the tile is legal_move, but do the weights add up
                        #boardArray[i].weights[1] == 1

                        # moved = the tile selected by player 1
                        try:
                            moved = selected_p1.pop()
                            boardArray[i].move_tile(moved)
                            boardArray[i].active = True
                            # Indicates that p1's turn is over
                            turn_player1 = False
                            boardArray[i].mouse_click = True
                            print("Player 2: Make your move")
                        except IndexError:
                            print 'Player 1 must go first'
                            break
                        # Player 1's turn is over
                    elif not turn_player1 and boardArray[i].legal_move:
                        # Yes the tile is legal_move, but do the weights add up

                        # AI player chooses which tile to play on main board

                        # Error if player doesnt select from the Player 2 field
                        try:
                            moved = selected_p2.pop()
                            boardArray[i].move_tile(moved)
                            boardArray[i].active = True
                        # Player 2's turn is over
                            turn_player1 = True
                            boardArray[i].mouse_click = True
                            print("Player 1: Make your move")
                        except IndexError:
                            print "Player 1's turn"

#   SIMULATE    ###########################################

    # Player 1 mouse handler
    for tile in player1Board:
        if tile.rect.collidepoint(pygame.mouse.get_pos()):
            tile.mouse_hover = True
        else:
            tile.mouse_hover = False

    # Player 2 mouse handler
    for tile in player2Board:
        if tile.rect.collidepoint(pygame.mouse.get_pos()):
            tile.mouse_hover = True
        else:
            tile.mouse_hover = False

    # Whiteboard mouse handler
    for tile in whiteBoard:
        if tile.rect.collidepoint(pygame.mouse.get_pos()):
            tile.mouse_hover = True
        else:
            tile.mouse_hover = False

    legal_tiles = []  # list that saves all legal tiles real_position

    # If the mouse is within the main board's tile rectangle, set color flag
    for tile in boardArray:
        if tile.rect.collidepoint(pygame.mouse.get_pos()):
            if selected_p1 or selected_p2:
                tile.mouse_hover = True
        else:
            tile.mouse_hover = False

        # Check for available moves, set tiles to legal_color
        if tile.active:
            if tile.weights[0] == 1:  # The top of the tile has a open path
                legal_tiles.append((tile.real_position[0], tile.real_position[1] - 1))

            if tile.weights[1] == 1:  # The right of the tile has a open path
                legal_tiles.append((tile.real_position[0] + 1, tile.real_position[1]))

            if tile.weights[2] == 1:  # The bottom of the tile has a open path
                legal_tiles.append((tile.real_position[0], tile.real_position[1] + 1))

            if tile.weights[3] == 1:  # The left of the tile has a open path, was + 1
                legal_tiles.append((tile.real_position[0] - 1, tile.real_position[1]))

#   UPDATE      ################################################
    for tile in boardArray:
        # Compare each tile with all tiles in legal_tiles list for legal moves
        for i in range(len(legal_tiles)):
            if tile.real_position == legal_tiles[i]:
                tile.legal_move = True
        tile.update()

    for tile in player1Board:
        # If rotate button is clicked and
        if rotate.active and tile.mouse_click and turn_player1:
            tile.shift_orientation()
            rotate.active = False
            tile.mouse_click = False
            # Add newly rotated tile to list
            selected_p1.pop()                   # ERROR ON THIS STATEMENT IN SOME CASES
            selected_p1.append(tile)
        tile.update()

    for tile in player2Board:
        if rotate.active and tile.mouse_click and not turn_player1:
            tile.shift_orientation()
            rotate.active = False
            tile.mouse_click = False
            # Add newly rotated tile to list
            selected_p2.pop()
            selected_p2.append(tile)
        tile.update()

    for tile in whiteBoard:
        if rotate.active and tile.mouse_click:
            tile.shift_orientation()
            rotate.active = False
            tile.mouse_click = False
            # Add newly rotated tile to list
            if turn_player1:
                selected_p1.pop()
                selected_p1.append(tile)
            else:
                selected_p2.pop()
                selected_p2.append(tile)
        tile.update()

#   DRAW        #####################################
    screen.fill((0, 0, 0))

    for tile in boardArray:
        tile.draw(screen)

    for tile in player1Board:
        tile.draw(screen)

    for tile in player2Board:
        tile.draw(screen)

    for tile in whiteBoard:
        tile.draw(screen)

    # GAME OVER CHECK
    # Two conditions; no tiles left or no legal moves
    moves_left = 0
    player1_points = 0
    player2_points = 0
    for tile in boardArray:
        if tile.player == 1:
            player1_points += 1
        if tile.player == 2:
            player2_points += 1

        if tile.legal_move and not tile.active:
            moves_left += 1

    if moves_left == 0:
        print("There are no moves left: GAME OVER")
        if player1_points > player2_points:
            screen.blit(p1_wins, 500,300)
            print("\t\tPlayer 1 wins!")

    # End of GAME OVER CHECK ####################

    # Draws Celtic! extra images
    screen.blit(title, (190, 0))
    screen.blit(scores_notes, (736, 0))  # 736, 468
    screen.blit(pieces_rules, (736, 288))  # 736, 180

    # Draws rotate button
    rotate.draw(screen)
    pygame.display.flip()
