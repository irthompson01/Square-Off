import sys, copy
import os
import simpleaudio as sound
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QGradient
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QLine, QPoint
from Score import Score
from Board import Board
from Tile import Tile
from Box import Box

# https://developer.mozilla.org/en-US/docs/Games/Introduction
cwd = os.getcwd()

class SquareOff(QWidget):

    def __init__(self, board):
      super().__init__()
      self.__board = board
      self.__sounds = [sound.WaveObject.from_wave_file(cwd+'/sounds/button.wav'),
                        sound.WaveObject.from_wave_file(cwd+'/sounds/Chime.wav'),
                        sound.WaveObject.from_wave_file(cwd+'/sounds/fart-01.wav')]

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
        qp.fillRect(0, 0, 1500, 1000, self.__gradients[2])
        #print("Yeah--", os.path.dirname(sys.executable))
        #qp.fillRect(1000, 0, 1500, 1000, self.__gradients[1])

        # fill tiles
        self.__board.color_tiles(qp)

        # Draw grid
        if self.__grid_lines is True:
            pen = QPen()
            pen.setColor(QColor(70,70,70))
            pen.setWidth(2)
            qp.setPen(pen)
            self.__board.draw_grid(qp)
            # Draw Medians
            pen.setWidth(5)
            qp.setPen(pen)
            qp.drawRect(QRect(self.__board.origin_x, self.__board.origin_y, self.__board.total_width, self.__board.total_width))
            qp.drawLine(QPoint(self.__board.origin_x, (self.__board.origin_y+(self.__board.total_width/2))), QPoint(self.__board.origin_x+self.__board.total_width,(self.__board.origin_y+(self.__board.total_width/2))))
            qp.drawLine(QPoint((self.__board.origin_x+(self.__board.total_width/2)), self.__board.origin_y), QPoint((self.__board.origin_x+(self.__board.total_width/2)), self.__board.origin_y+self.__board.total_width))


        # Draw Boxes
        self.__board.draw_boxes(qp)

        # Draw New Boxes
        self.__board.draw_new_boxes(qp)

        # Display Score
        qp.setPen(self.__blackPen)
        self.__board.display_score(qp)

        # Draw Line Toggle Buttons
        self.__board.draw_line_toggle(qp)

        # Draw Reset Tile
        self.__board.draw_reset_box(qp)

        qp.end()

    def mousePressEvent(self, event):

        mpx = event.x()
        mpy = event.y()

        # Check if reset board
        if self.__board.is_inside_reset(mpx, mpy):
            self.__sounds[2].play()
            self.__board.reset_board()

        # Check if inside playing grid
        if self.__board.is_inside_grid(mpx, mpy):

            is_valid = self.__board.grid_click(mpx, mpy)

            # Checking if the square selected is not occupied
            if is_valid:
                # Play button click
                self.__sounds[0].play()

                # Loop for new boxes formed
                self.__board.find_new_boxes()

                # Play new box chime if new squares are formed
                if len(self.__board.current_player.new_boxes) > 0:
                    self.__sounds[1].play()
                    self.__board.current_player.line_toggle = True

                # Update Score
                self.__board.update_score()

                # Move to next players turn
                self.__board.next_player()

            # Occupied square selected, Same Turn
            else:
                self.__grid_lines = not self.__grid_lines

        else: # Check for line toggle buttons
            for player in self.__board.players:
                if player.inside_tile(mpx, mpy):
                    player.line_toggle = not player.line_toggle


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
