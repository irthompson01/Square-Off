#################
### BOX CLASS ###
#################
from PyQt5.QtCore import Qt, QRect, QLine, QPoint
from Score import Score

'''
A Rotated Box object is a collection of tiles that form a 90 deg rotated equalateral box that earns double points
'''

class Rot_Box:

    def __init__(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

        self.top_x = top.origin_x + (top.length / 2)
        self.top_y = top.origin_y + (top.length / 2)
        self.left_x = left.origin_x + (left.length / 2)
        self.left_y = left.origin_y + (left.length / 2)
        self.bottom_x = bottom.origin_x + (bottom.length / 2)
        self.bottom_y = bottom.origin_y + (bottom.length / 2)
        self.right_x = right.origin_x + (right.length / 2)
        self.right_y = right.origin_y + (right.length / 2)

        self.size = ((top.origin_x - left.origin_x) / top.length) + 1
        self.points = self.size*self.size*2
        self.new_box = True

    def check_ownership(self):

        if (self.top.occupant == self.left.occupant and \
            self.left.occupant == self.bottom.occupant and \
            self.bottom.occupant == self.right.occupant and \
            self.right.occupant != None):

            if self.new_box:
                #print("------------", self.top_left.occupant, self.top_right.occupant, self.bottom_left.occupant, self.bottom_right.occupant)
                self.new_box = False
                return True

        else:
            return False

    def draw_box(self, qp):
        qp.drawLine(QPoint(self.top_x, self.top_y), QPoint(self.left_x, self.left_y))
        qp.drawLine(QPoint(self.left_x, self.left_y), QPoint(self.bottom_x, self.bottom_y))
        qp.drawLine(QPoint(self.bottom_x, self.bottom_y), QPoint(self.right_x, self.right_y))
        qp.drawLine(QPoint(self.right_x, self.right_y), QPoint(self.top_x, self.top_y))
