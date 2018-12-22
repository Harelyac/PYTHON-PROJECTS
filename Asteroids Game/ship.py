import math
import random

START_DIRECTION = 0  # degrees units only
CHNAGE_DIRECTION_VALUE = 7  # degrees units only
SPACE_SHIP_RADIUS = 1


class Ship:
    """
    This class represent a ship object in the asteroids game.
    """

    def __init__(self):
        self.__x_axis_location = random.randint(-500, 500)
        self.__y_axis_location = random.randint(-500, 500)
        self.__x_axis_speed = 0
        self.__y_axis_speed = 0
        self.__heading = START_DIRECTION

    def radius(self):
        return SPACE_SHIP_RADIUS

    def change_direction_right(self):
        """

        :return:
        """
        self.__heading -= CHNAGE_DIRECTION_VALUE

    def change_direction_left(self):
        """

        :return:
        """
        self.__heading += CHNAGE_DIRECTION_VALUE

    def accelerate_ship(self):
        """

        :return:
        """
        # convert angle from degree to radians
        new_x_speed = self.__x_axis_speed + \
                      math.cos(math.radians(self.__heading))
        self.__x_axis_speed = new_x_speed
        new_y_speed = self.__y_axis_speed + \
                      math.sin(math.radians(self.__heading))
        self.__y_axis_speed = new_y_speed

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

    def set_x_axis_coordinate(self, value):
        self.__x_axis_location = value

    def set_y_axis_coordinate(self, value):
        self.__y_axis_location = value
