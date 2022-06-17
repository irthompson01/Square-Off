import sys, copy
import simpleaudio as sound
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QGradient
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QLine
from Score import Score
from Board import Board
from Tile import Tile
from Box import Box

class SquareOff(QWidget):

    def __init__(self, board):
      super().__init__()
      self.__board = board
      self.__gradients = [QGradient(16), # Deep Blue - 0
                            QGradient(34), # Lemon Gate - 1
                            QGradient(107), # Confident Cloud - 2
                            QGradient(116), # Above The Sky - 3
                            QGradient(121), # Marble Wall - 4
                            QGradient(124), # Magic Lake - 5
                            QGradient(145) # Rich Metal - 6
                            ]
      self.__blackPen = QPen(QBrush(Qt.black),3)
      self.__green = QBrush(QColor(102,255,255))
      self.__yellow = QBrush(QColor(255, 163, 102))

      self.__grid_lines = True

      self.setGeometry(50, 50, 1500, 1000)
      self.setWindowTitle('Square Off')
      self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # https://webgradients.com/
        qp.fillRect(0, 0, 1500, 1000, self.__gradients[6])
        #qp.fillRect(1000, 0, 1500, 1000, self.__gradients[1])

        # fill tiles
        self.__board.color_tiles(qp)

        # Draw grid
        if self.__grid_lines is True:
            qp.setPen(self.__blackPen)
            self.__board.draw_grid(qp)

        # Draw Boxes
        self.__board.draw_boxes(qp)

        # Display Score
        qp.setPen(self.__blackPen)
        self.__board.display_score(qp)

        # Draw Line Toggle Buttons

        self.__board.draw_line_toggle(qp)

        qp.end()

    def mousePressEvent(self, event):

        mpx = event.x()
        mpy = event.y()


        # Check if inside playing grid
        if self.__board.is_inside_grid(mpx, mpy):

            is_valid = self.__board.grid_click(mpx, mpy)

            # Checking if the square selected is not occupied
            if is_valid:
                # Loof for new boxes formed
                self.__board.find_new_boxes()

                # Update Score
                self.__board.update_score()

                # Move to next players turn
                self.__board.next_player()

            # Occupied square selected, Same Turn
            else:

                pass

        else: # Check for line toggle buttons
            for player in self.__board.players:
                if player.inside_tile(mpx, mpy):
                    player.line_toggle = not player.line_toggle
                    print(player.line_toggle)
            self.__grid_lines = True#not self.__grid_lines

        self.update()

if __name__ == '__main__':
  app = QApplication(sys.argv)

  try:
      size = int(sys.argv[1])
      num_players = int(sys.argv[2])
      board = Board(size=size, num_players=num_players)
  except:
      board = Board()
      
  ex = SquareOff(board)
  sys.exit(app.exec_())
