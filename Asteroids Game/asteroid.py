import math
import random

SECOND_ASTEROID = 1
SPLIT = 2
SIZE_FACTOR = 10
DEFAULT_ASTEROIDS_NUM = 5
############################################################
# Class definition
############################################################
class Asteroid:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self):
        """
        Initialize a new Game object.
        :return: A new Game object.
        """
        self.__x_axis_location = random.randint(-500, 500)
        self.__y_axis_location = random.randint(-500, 500)
        self.__x_axis_speed = random.randint(-10, 10)
        self.__y_axis_speed = random.randint(-10, 10)
        self.__size = 3

    def radius(self):
        return (self.__size * SIZE_FACTOR) - DEFAULT_ASTEROIDS_NUM

    def has_intersection(self, object):
        distance = math.sqrt((object.get_x_axis_coordinate() - self.__x_axis_location)**2 +
                             ((object.get_y_axis_coordinate() - self.__y_axis_location)**2))
        if distance <= self.radius() + object.radius():
            return True
        else:
            return False

    def terminated(self):
        if self.__size <= 0:
            return True
        else:
            return False

    def get_x_axis_coordinate(self):
        return self.__x_axis_location

    def get_y_axis_coordinate(self):
        return self.__y_axis_location

    def get_x_speed(self):
        return self.__x_axis_speed

    def get_y_speed(self):
        return self.__y_axis_speed

    def get_size(self):
        return self.__size

    def set_x_axis_coordinate(self, value):
        self.__x_axis_location = value

    def set_y_axis_coordinate(self, value):
        self.__y_axis_location = value

    def set_size(self, value):
        self.__size = value

    def set_x_speed(self, value):
        self.__x_axis_speed = value

    def set_y_speed(self, value):
        self.__y_axis_speed = value
