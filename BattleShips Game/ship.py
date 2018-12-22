import ship_helper as sh


############################################################
# Helper class
############################################################


class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    NOT_MOVING = " "  # space

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)


############################################################
# Class definition
############################################################


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = pos
        self.__length = length
        self.__direction = direction
        self.__board_size = board_size
        # make a list of all ship's coordinates
        self.__ship_coordinates = self.coordinates()
        # make a dictionary that indicate status of a ship
        self.__ship_coordinates_status = self.get_ship_coord_status()

    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)).
        The tuple's content should be (in the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """

        # Gets all coordinates of ship in a list
        ship_coordinates = self.__ship_coordinates
        # Gets all damaged ship coordinates
        damaged_coordinates = self.damaged_cells()
        # Gets string value of last direction
        last_direction = sh.direction_repr_str(Direction, self.direction())
        # Make the duple needed
        represent = (ship_coordinates, damaged_coordinates, last_direction,
                     self.__board_size)
        # Return after converting to str!
        return str(represent)

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement
        would take the ship outside of the board, in which case
        the ship switches direction and sails one board
        unit in the new direction.
        :return: A direction object representing the current movement direction.
        """

        # First check collisions and change direction if necessary
        self.check_collision()

        # Then move ship 1 board unit only if
        # none of the ship coordinate is hit!
        if self.__direction != Direction.NOT_MOVING:
            if self.__direction == Direction.UP:
                self.__pos = self.__pos[0], self.__pos[1] - 1
                self.__ship_coordinates = self.coordinates()
            elif self.__direction == Direction.DOWN:
                self.__pos = self.__pos[0], self.__pos[1] + 1
                self.__ship_coordinates = self.coordinates()
            elif self.__direction == Direction.RIGHT:
                self.__pos = self.__pos[0] + 1, self.__pos[1]
                self.__ship_coordinates = self.coordinates()
            elif self.__direction == Direction.LEFT:
                self.__pos = self.__pos[0] - 1, self.__pos[1]
                self.__ship_coordinates = self.coordinates()

            # Update the status ship dict accordingly
            self.__ship_coordinates_status = self.get_ship_coord_status()

        return self.__direction

    def check_collision(self):
        """
        this function checks collision of ships with the game board and change
        direction accordingly.
        :return:
        """

        last_pos = self.coordinates()[-1]

        # check for collision and change direction accordingly

        # Check for collision right side of board
        if last_pos[0] == self.__board_size - 1 and \
                        self.__direction == Direction.RIGHT:
            self.change_direction()
        # Check for collision on bottom side of the board
        elif last_pos[1] == self.__board_size - 1 and \
                        self.__direction == Direction.DOWN:
            self.change_direction()
        # Check for collision on the left side of the board
        elif self.__pos[0] == 0 and self.__direction == Direction.LEFT:
            self.change_direction()
        # Check for collision on the upper side of the board
        elif self.__pos[1] == 0 and self.__direction == Direction.UP:
            self.change_direction()

    def change_direction(self):
        """
        This function set the opposite direction of an instance. kind of
        reversing direction!
        """
        if self.__direction == Direction.DOWN:
            self.__direction = Direction.UP
        elif self.__direction == Direction.UP:
            self.__direction = Direction.DOWN
        elif self.__direction == Direction.LEFT:
            self.__direction = Direction.RIGHT
        elif self.__direction == Direction.RIGHT:
            self.__direction = Direction.LEFT

    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        # Check if hit pos is on one of the ship coordinates
        if pos in self.__ship_coordinates:
            # Check if this coord of ship was already hit!
            if self.__ship_coordinates_status[pos]:
                return False
            else:
                # Change status of ship coordinate
                self.__ship_coordinates_status[pos] = True

                # Stop ship from moving in the next game round
                self.__direction = Direction.NOT_MOVING

                return True
        else:
            return False

    def get_ship_coord_status(self):
        """
        Make first initialization of ship coordinates status to True
        and then each time the ship moves or hit it update
        the coordinates and accordingly
        :return:
        """
        # Make a dict contain the status of each coordinate of ship
        return {coordinate: False for coordinate in self.__ship_coordinates}

    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns,
        False otherwise.
        """

        if all(value is True for value in
               self.__ship_coordinates_status.values()):
            return True
        else:
            return False

    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinate, False otherwise.
        """

        # get all ship coordinates
        if pos in self.__ship_coordinates:
            return True
        else:
            return False

    def coordinates(self):
        """
        Return ship's current coordinates on board.
        :return: A list of (x, y) tuples representing the ship's current
        occupying coordinates.
        """

        all_ship_coordinates = list()

        # append fist trivial and minimal coordinate
        all_ship_coordinates.append(self.__pos)

        # The coordinate to move on all other coordinates - start point
        ship_coordinate = self.__pos

        # go on all coordinates of a ship
        for coordinate in range(self.__length - 1):
            # Make ship coordinate as list to start work with

            if self.direction() in Direction.VERTICAL:
                ship_coordinate = ship_coordinate[0], ship_coordinate[1] + 1
                all_ship_coordinates.append(ship_coordinate)
            elif self.direction() in Direction.HORIZONTAL:
                ship_coordinate = ship_coordinate[0] + 1, ship_coordinate[1]
                all_ship_coordinates.append(ship_coordinate)

        # return list of all ship coordinates
        return all_ship_coordinates

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        # Make the list of all coord which are damaged
        damaged_ship_coordinates = \
            [coord for coord in self.__ship_coordinates_status if
             self.__ship_coordinates_status[coord] is True]
        return damaged_ship_coordinates

    def not_damaged_cells(self):
        """
        Return the ship's not hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were not hit in past turns (If there are hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        # Make the list of all coord which are damaged
        not_damaged_ship_coordinates = \
            [coord for coord in self.__ship_coordinates_status if
             self.__ship_coordinates_status[coord] is False]
        return not_damaged_ship_coordinates

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current sailing direction or
         NOT_MOVING if the ship is hit and not moving.
        """
        # Check if ship collide in the last round and
        # return the previous direction
        return self.__direction

    def cell_status(self, pos):
        """
        Return the status of the given coordinate (hit\not hit) in current
        ship.
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        if not self.__contains__(pos):
            return None
        else:
            if not self.__ship_coordinates_status[pos]:
                return False
            else:
                return True


