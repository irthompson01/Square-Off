#################
### BOX CLASS ###
#################
from PyQt5.QtCore import Qt, QRect, QLine
from Score import Score

'''
A Box object is a collection of tiles that form an equalateral box that earns points
'''

class Box:

    def __init__(self, top_left, top_right, bottom_left, bottom_right):

        self.occupant = None
        self.length = top_right.origin_x - top_left.origin_x
        self.size = (self.length / top_right.length) + 1
        self.points = self.size*self.size
        self.origin_x = top_left.origin_x + (top_left.length / 2)
        self.origin_y = top_left.origin_y + (top_left.length / 2)
        self.QRect = QRect(self.origin_x, self.origin_y, self.length, self.length)
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.new_box = True

    def check_ownership(self):

        if (self.top_left.occupant == self.top_right.occupant and \
            self.top_right.occupant == self.bottom_left.occupant and \
            self.bottom_left.occupant == self.bottom_right.occupant and \
            self.bottom_right.occupant != None):

            if self.new_box:
                #print("------------", self.top_left.occupant, self.top_right.occupant, self.bottom_left.occupant, self.bottom_right.occupant)
                self.new_box = False
                return True

        else:
            return False

    def draw_box(self, qp):
        qp.drawRect(self.QRect)
