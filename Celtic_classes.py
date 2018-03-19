import pygame
import math
import copy

SCREEN_width = 1024
SCREEN_height = 768
TILESIZE_width = 70
TILESIZE_height = 68

player1_color = (255, 0, 0)     # RED
player2_color = (0, 0, 255)     # BLUE
selected_color = (255, 255, 0)  # YELLOW
idle_color = (0, 137, 68)       # GREEN
legal_color = (255, 118, 49)      # ORANGE


#  Vector2     ######
class vector2:
    #   Param constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):  # Negates a vector
        v = vector2(-self.x, -self.y)
        return v

    # method definitions
    def add(self, other):
        v = vector2(self.x + other.x, self.y + other.y)
        return v

    def sub(self, other):
        v = vector2(self.x - other.x, self.y - other.y)
        return v

    def scale(self, s):
        ans = vector2(self.x, self.y)
        ans.x *= s
        ans.y *= s
        return ans

    def magn(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        result = vector2(0, 0)
        m = self.magn()
        if m == 0:
            return vector2(0, 0)
        result.x = self.x / m
        result.y = self.y / m
        return result

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # overload return-this-as-string for printing
    def __str__(self):
        # format allows you to replace "{}" with variable values
        return "({}, {})".format(self.x, self.y)

#   End of VECTOR2   #########


class TileBoard:    # May need to add player in order to see who won
    def __init__(self, pos, color, column, row):
        self.image = None
        self.MARGIN = 1  # how far away each action is left to right, ex width margin width
        self.size = (TILESIZE_width, TILESIZE_height)
        self.position = pos
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
        self.col = column
        self.row = row
        self.player = None
        self.img_size = None
        self.img_position = None
        self.mouse_hover = False
        self.mouse_click = False
        self.color = color
        self.active = False
        self.id = None
        self.weights = None     # Weight order = Top, Left, Bottom, Right
        self.orientation = 0  # 0 is the default orientation, increased value += 90' clockwise shift

        # Used to check if a legal move is present
        self.legal_move = False
        self.real_position = (column, row)   # Stores coordinate position in board

    def tile_setup(self, tile_id, player, rotate):   # This should only be called once per new tile
        self.id = tile_id
        self.player = player
        image_file = ""

        # Based on id, and player number, set paths and images
        if self.player == 1:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadend.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twoway.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threeway.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/corner.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourway.png"

        if self.player == 2:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadendB.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twowayB.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threewayB.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/cornerB.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourwayB.png"

        if self.player == 3:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadendW.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twowayW.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threewayW.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/cornerW.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourwayW.png"

        self.image = pygame.image.load(image_file)
        self.active = True

        self.img_size = [int(x * 1) for x in self.image.get_size()]  # x * [size rescaling]
        self.img_position = (self.position.x, self.position.y)

        for i in range(rotate):
            self.shift_orientation()

    def move_tile(self, other_tile):
        # used when tile is moved from the original position to the board
        # or vise versa
        self.tile_setup(other_tile.id, other_tile.player_number, other_tile.orientation)

    def shift_orientation(self):
        # Shift their paths clockwise once
        self.image = pygame.transform.rotate(self.image, -90)

        # Copy weights[] to shiftList[]
        shiftList = copy.deepcopy(self.weights)
        shiftList = shiftList[3:] + shiftList[:3]
        self.weights = copy.deepcopy(shiftList)

    def destroy(self):
        # Removes all data that makes a tile active
        self.active = False
        self.image = None
        self.weights = [0, 0, 0, 0]
        self.color = idle_color
        self.img_size = None
        self.img_position = None
        self.orientation = 0
        self.id

    def update(self):

        if self.legal_move:
            self.color = legal_color
        # Player has mouse over this tile
        elif self.mouse_hover | self.mouse_click:
            self.color = selected_color
        else:
            self.color = idle_color

        # Player has selected this tile (mouse click)
        #if self.active:
        #    self.color = selected_color

    def draw(self, scr):
        #   Draws rect same size as image, exclude to stop drawing to screen
        pygame.draw.rect(scr, self.color, self.rect)

        # Blit the image surface to screen surface
        # Active, meaning square has an assigned tile
        if self.active:
            scr.blit(self.image, (self.position.x + self.MARGIN, self.position.y + self.MARGIN))
        #else:
        #    scr.blit(self.image, (self.img_position[0] + self.MARGIN, self.img_position[1] + self.MARGIN))

# ----END OF TILE CLASS----###################


class TilePlayer:
    def __init__(self, pos, tile_color, pNum):
        self.image = None
        self.MARGIN = 1  # how far away each action is left to right, ex width margin width
        self.position = pos
        self.size = (TILESIZE_width, TILESIZE_height)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
        self.mouse_hover = False
        self.mouse_click = False
        self.color = tile_color
        self.player_number = pNum
        self.img_size = None
        self.img_position = None
        self.active = False  # Space contains a tile
        self.board_place = None

        # Used to set whether a path is available, 0 = no path, 1 = path
        self.weights = None
        self.id = None
        self.orientation = 0  # 0' is the default orientation, increased value += 90' clockwise shift

    def tile_setup(self, tile_id):   # This should only be called once per new tile
        self.id = tile_id
        image_file = ""

        # Based on id, and player number, set paths and images
        if self.player_number == 1:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadend.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twoway.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threeway.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/corner.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourway.png"

        if self.player_number == 2:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadendB.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twowayB.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threewayB.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/cornerB.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourwayB.png"

        if self.player_number == 3:
            # Check tile id
            if self.id == 00:  # Dead End Tile
                self.weights = [0, 0, 1, 0]
                image_file = "imgs/deadendW.png"

            elif self.id == 01:  # Two Way Tile
                self.weights = [1, 0, 1, 0]
                image_file = "imgs/twowayW.png"

            elif self.id == 02:  # Three Way Tile
                self.weights = [0, 1, 1, 1]
                image_file = "imgs/threewayW.png"

            elif self.id == 03:  # Corner Tile
                self.weights = [0, 1, 1, 0]
                image_file = "imgs/cornerW.png"

            elif self.id == 04:  # Four Way Tile
                self.weights = [1, 1, 1, 1]
                image_file = "imgs/fourwayW.png"

        self.image = pygame.image.load(image_file)
        self.active = True

        self.img_size = [int(x * 1) for x in self.image.get_size()]  # x * [size rescaling]
        self.img_position = (self.position.x, self.position.y)

    def shift_orientation(self):
        # Shift their paths clockwise once
        self.image = pygame.transform.rotate(self.image, -90)
        self.orientation += 1

        # Copy weights[] to shiftList[]
        shiftList = copy.deepcopy(self.weights)
        shiftList = shiftList[3:] + shiftList[:3]
        self.weights = copy.deepcopy(shiftList)

    def is_legal(self):
        pass

    def update(self):
        if self.mouse_hover | self.mouse_click:
            self.color = selected_color
        else:
            if self.player_number == 1:
                self.color = player1_color
            elif self.player_number == 2:
                self.color = player2_color
            else:
                self.color = legal_color

    def draw(self, scr):
        # Draws rect same size as image, exclude to stop drawing to screen
        pygame.draw.rect(scr, self.color, self.rect)

        # Blit the image surface to screen surface when active
        if self.active:
            scr.blit(self.image, (self.position.x + self.MARGIN, self.position.y + self.MARGIN))
        else:
            pass
# ----END OF TILE CLASS----###################


class rotateButton:
    def __init__(self, img, pos):
        self.image = img
        self.size = [int(x * 1) for x in self.image.get_size()]
        self.position = pos
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
        self.active = False

    def draw(self, scr):
        #pygame.draw.rect(scr, (255, 0, 255), self.rect)
        scr.blit(self.image, (self.position.x, self.position.y))

class celtic_ai:
    def __init__(self):
        self.state = None
        self.move_list = None

    def add_move(self, new_tile):
        # move_list.append(new_tile)
        pass
