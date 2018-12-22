ACCELERATOR_FACTOR = 2
RADIUS = 4
MAX_STEPS = 200

#######################################################################################################################
from screen import Screen
import math
#######################################################################################################################

class Torpedo:
    """
    This class represent a torpedo object in the asteroids game.
    """
    def __init__(self, x_ship_location, y_ship_location, x_ship_speed, y_ship_speed, ship_heading ):
        self.__x_axis_location = x_ship_location
        self.__y_axis_location = y_ship_location
        self.__x_axis_speed = x_ship_speed + (ACCELERATOR_FACTOR * math.cos(math.radians(ship_heading)))
        self.__y_axis_speed = y_ship_speed + (ACCELERATOR_FACTOR * math.sin(math.radians(ship_heading)))
        self.__heading = ship_heading
        self.__steps = 0

    def radius(self):
        return RADIUS

    def get_x_axis_coordinate(self):
        return self.__x_axis_location

    def get_y_axis_coordinate(self):
        return self.__y_axis_location

    def get_heading(self):
        return self.__heading

    def get_x_speed(self):
        return self.__x_axis_speed

    def get_y_speed(self):
        return self.__y_axis_speed

    def set_x_axis_coordinate(self,value):
        self.__x_axis_location = value

    def set_y_axis_coordinate(self,value):
        self.__y_axis_location = value

    def add_steps(self):
        self.__steps += 1

    def get_steps(self):
        return self.__steps

    def max_steps(self):
        return MAX_STEPS