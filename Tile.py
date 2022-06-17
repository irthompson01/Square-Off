### Tile
###
### -> QRect
###
from PyQt5.QtCore import Qt, QRect, QLine
#from Score import Score

class Tile:

    def __init__(self, origin_x, origin_y, length):

        self.occupant = None
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.length = length
        self.QRect = QRect(self.origin_x, self.origin_y, self.length, self.length)

    def set_occupant(self, player):
        self.occupant = player

    def fill_tile(self):
        pass

    def __str__(self):
        return "Origin X: " + str(self.origin_x) + " Origin Y: " + str(self.origin_y) + " Length: " + str(self.length) + " Occupant: " + str(self.occupant)
