from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PyQt5.QtCore import Qt, QRect, QLine
from Tile import Tile
import math

class Score:

  def __init__(self, player_name, color = [0,0,0]):
    self.__player_name = str(player_name+1)
    self.__current_score = 0
    self.__current_level = 0
    self.__current_multiplier = 1
    self.__lives_remaining = 3
    self.__show_boxes = True
    self.line_toggle = True
    self.line_tile = Tile(950+(100*player_name), 100, 100)
    self.squares_formed = 0
    self.boxes = []
    self.new_boxes = []
    self.outline_color = QColor(color[0], color[1], color[2], 127)
    self.fill_color = QBrush(QColor(color[0], color[1], color[2], 200))

  def inside_tile(self, mpx, mpy):
      if mpx >= self.line_tile.origin_x and \
        mpx <= (self.line_tile.origin_x + self.line_tile.length) and \
         mpy >= self.line_tile.origin_y and \
          mpy <= (self.line_tile.origin_y + self.line_tile.length):
          return True
      else:
          return False


  def add_points(self, amount):
    self.__current_score += (self.__current_multiplier)*amount
    if(0<=self.__current_score<10000):
      self.__current_level = 0
    else:
      self.__current_level = math.ceil(math.log((self.__current_score/10000), 2))
    return self.__current_score


  def subtract_points(self, amount):
    self.__current_multiplier = 1
    self.__current_score -= amount
    if(self.__current_score<10000):
      self.__current_level = 0
    else:
      self.__current_level = math.ceil(math.log((self.__current_score/10000), 2))
    return self.__current_score

  def get_multiplier(self):
    return self.__current_multiplier

  def increment_multiplier(self, amount):
    self.__current_multiplier += amount
    return self.__current_multiplier

  def reset_multiplier(self):
      self.__current_multiplier = 1

  def get_score(self):
    return self.__current_score

  def get_level(self):
    return self.__current_level

  def get_lives(self):
    return self.__lives_remaining

  def lose_life(self):
    if(self.__lives_remaining > 0):
      self.__lives_remaining -= 1
      return True
    else:
      return False

  def gain_life(self):
    self.__lives_remaining += 1

  def get_player_name(self):
    return self.__player_name

  def get_stats(self):
    return 'Player: ' + str(self.__player_name) + ', ' + 'Score: ' + str(int(self.__current_score)) + ', ' + 'Multiplier: '+ str(self.__current_multiplier)


  def __str__(self):
    return 'Player: ' + str(self.__player_name) + ', ' + 'Score: ' + str(self.__current_score) + ', ' + 'Multiplier: '+ str(self.__current_multiplier)

# if __name__ == '__main__':
#   #TODO replace pass with your tests for your Score object.
#   game = Score('Hodor')
#   print(game)
#   game.add_points(100000)
#   game.increment_multiplier()
#   game.add_points(200000)
#   game.lose_life()
#   game.lose_life()
#   game.lose_life()
#   print(game)
#   game.subtract_points(350000)
#   print(game.get_score())
#   print(game)
#   game.lose_life()
#   print(game.lose_life())
#   print(game.get_level())
#   print(game.get_multiplier())
