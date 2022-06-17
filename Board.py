###################
### BOARD CLASS ###
###################
from PyQt5.QtCore import Qt, QRect, QLine
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
import numpy as np
from Score import Score
from Tile import Tile
from Box import Box
from Rot_Box import Rot_Box
'''
A Board
'''

class Board:

    def __init__(self, size=8, num_players=2):
        self.total_width = 800
        self.width = size
        self.height = size
        self.tile_length = self.total_width / size
        self.origin_x = 100
        self.origin_y = 100
        self.num_players = num_players
        # self.colors = [
        #         [17, 87, 64],
        #         [185, 151, 91],
        #         [229, 106, 84],
        #         [24, 48, 40]
        # ]
        self.colors = [list(np.random.choice(range(255),size=3)) for i in range(num_players)]
        self.players = [Score(i, self.colors[i]) for i in range(0, num_players)]
        self.current_player = self.players[0]

        self.grid = [[Tile(self.origin_x + (self.tile_length*i), self.origin_y+ (self.tile_length*j), self.tile_length)
                      for i in range(0,self.width)]
                     for j in range(0, self.height)]

        self.boxes = [ [Box(self.grid[i][j],
                    self.grid[i][j+num],
                    self.grid[i+num][j],
                    self.grid[i+num][j+num]) for i in range(0, self.width - num) for j in range(0, self.height - num)] for num in range(1, self.width)]


        self.rot_boxes = [ [Rot_Box(self.grid[i][j+int(num)],
                        self.grid[i+num][j],
                        self.grid[i+int(2*num)][j+num],
                        self.grid[i+num][j+int(2*num)]) for i in range(0, self.width - int(2*num)) for j in range(0, self.height - int(2*num))] for num in range(1, self.width//2) ]


        self.all_boxes = self.boxes + self.rot_boxes

    def next_player(self):
        idx = (self.players.index(self.current_player) + 1) % self.num_players
        self.current_player = self.players[idx]

    def draw_grid(self, qp):
        #Loop through self.grid and draw as black
        for row in self.grid:
            for tile in row:
                qp.drawRect(tile.QRect)

    def draw_line_toggle(self, qp):
        for player in self.players:
            pen = QPen()
            pen.setColor(player.outline_color)
            pen.setWidth(3)
            pen.setJoinStyle(Qt.RoundJoin)
            qp.setPen(pen)
            #rect = QRect(950+(100*self.players.index(player)), 100, 100, 100)
            qp.drawRect(player.line_tile.QRect)
            if player.line_toggle:
                qp.fillRect(player.line_tile.QRect, player.fill_color)


    def color_tiles(self, qp):
        #Loop through self.grid and fillRect as
        for row in self.grid:
            for tile in row:
                player = tile.occupant
                if player is not None:
                    pen = QPen()
                    pen.setColor(player.outline_color)
                    pen.setWidth(3)
                    pen.setJoinStyle(Qt.RoundJoin)
                    qp.setPen(pen)
                    qp.drawRect(tile.QRect)
                    qp.fillRect(tile.QRect, player.fill_color)

    def find_new_boxes(self):
        for size in self.all_boxes:
            for box in size:
                if box.check_ownership():
                    self.current_player.squares_formed += 1
                    self.current_player.boxes.insert(0, box)
                    #print(self.current_player.boxes)

    def select_grid_tile(self, mpx, mpy):

        ox = mpx - ((mpx - self.origin_x) % self.tile_length)
        oy = mpy - ((mpy - self.origin_y) % self.tile_length)

        idx_x = int((ox / self.tile_length) - (self.origin_x//self.tile_length))
        idx_y = int((oy / self.tile_length) - (self.origin_x//self.tile_length))

        tile = self.grid[idx_y][idx_x]
        # print(mpx, mpy)
        # print("--------------")
        # print(ox, oy)
        # print("--------------")
        # print(idx_y, idx_x)
        # print("##############")
        return tile

    def is_inside_grid(self, mpx, mpy):
        if mpx >= self.origin_x and mpx <= self.origin_x + (self.width*self.tile_length) and mpy >= self.origin_y and mpy <= self.origin_y + (self.height*self.tile_length):
            return True

        else:
            return False

    def grid_click(self, mpx, mpy):
        tile = self.select_grid_tile(mpx, mpy)

        if tile.occupant == None:
            tile.set_occupant(self.current_player)

            return tile
        else:
            return False

    def draw_boxes(self, qp):
        for player in self.players:
            if player.line_toggle:
                for box in player.boxes:
                    pen = QPen()
                    pen.setColor(player.outline_color)
                    pen.setWidth(5)
                    pen.setStyle(Qt.DashLine)
                    pen.setJoinStyle(Qt.RoundJoin)
                    qp.setPen(pen)
                    box.draw_box(qp)

    def update_score(self):
        mult = self.current_player.squares_formed
        #print("Squares formed: ", mult)
        if mult <= 1:
            self.current_player.reset_multiplier()
        # Increment multiplier
        else:
            self.current_player.increment_multiplier(mult-1)

        # Add points using multiplier for all new squares
        for i in range(0, mult):
            points = self.current_player.boxes[i].points
            #print("Points: ", points)
            self.current_player.add_points(points)



        self.current_player.squares_formed = 0

    def display_score(self, qp):
        qp.setFont(QFont("Times", 15))
        for player in self.players:
            if player == self.current_player:
                qp.fillRect(950, 265+(100*self.players.index(player)), 500, 50, player.fill_color)

            qp.drawText(1000, 300+(100*self.players.index(player)), player.get_stats())
