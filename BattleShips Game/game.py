############################################################
# Imports
############################################################
import game_helper as gh
from copy import deepcopy


############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.__ships = ships
        self.__bombs = dict()
        self.__hits = list()
        self.__hit_ships = list()
        self.__not_hit_ships = list()

    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round
            (number of hits and terminated ships)
        :return:
            (some constant you may want implement which represents)
            Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """

        # Get target
        target = gh.get_target(self.__board_size)

        # Put the target on board
        self.put_target(target)

        # Move all ship that were not hit in last turn
        for ship in self.__ships:
            ship.move()

        # Check if ship was hit by an active bomb(also from last turns) need
        # to mention that this checking is made only after moving all ships!

        hit_count = 0

        # list of bombs that we should keep for future rounds
        bombs_to_delete = list()

        # Check if its a hit! and append a new hit to hit list. and also
        # count it.
        bombs_list_copy1 = deepcopy(self.__bombs)
        for ship in self.__ships:
            for bomb in bombs_list_copy1:
                # Check if there was a direct hit
                if ship.hit(bomb):
                    # Counter that count hits!
                    hit_count += 1
                    if bomb not in self.__hits:
                        self.__hits.append(bomb)
                    # add bomb to delete soon
                    bombs_to_delete.append(bomb)

        # For each ship distribute tuples accordingly if they are hit or not
        # each for the related list
        self.__hit_ships = []
        self.__not_hit_ships = []

        for ship in self.__ships:
            self.__hit_ships.extend(ship.damaged_cells())
            self.__not_hit_ships.extend(ship.not_damaged_cells())

        # lessen the span life of each bomb and delete the bombs with 1 span
        bombs_list_copy = deepcopy(self.__bombs)

        if self.__bombs:
            for bomb in bombs_list_copy:
                if self.__bombs[bomb] == 1:
                    del self.__bombs[bomb]
                else:
                    self.__bombs[bomb] -= 1

        # prints board to screen
        print(gh.board_to_string(self.__board_size, self.__hits,
                                 self.__bombs, self.__hit_ships,
                                 self.__not_hit_ships))

        # delete the bombs that hit a target or some of them.
        set(bombs_to_delete)
        for bomb in bombs_to_delete:
            if bomb in self.__bombs:
                del self.__bombs[bomb]

        bombs_to_delete = []

        # remove the terminated ships from game
        terminated = 0
        ship_list = list()

        # Remove last turn hit from hit list
        self.__hits = []

        for ship in self.__ships:
            if not ship.terminated():
                ship_list.append(ship)
            else:
                terminated += 1

        # Update the ship list
        self.__ships = ship_list

        # Report turn result to screen
        gh.report_turn(hit_count, terminated)

    def put_target(self, target):
        """
        This function puts bomb on specific coordinate on board
        :param target:
        :return:
        """
        self.__bombs[target] = 4

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        # Make big string of ships contain the identity of each ship on board.
        # put them all inside a tuple
        represent = (self.__board_size, self.__bombs, self.__ships)
        # return after converting to str
        return str(represent)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # Report game instructions
        gh.report_legend()

        # Initialize ship coordinate for display!
        list_of_ships_coordinates = list()

        for ship in self.__ships:
            list_of_ships_coordinates.extend(ship.coordinates())

        # print board to screen
        print(gh.board_to_string(self.__board_size, self.__hits,
                                 self.__bombs, self.__hit_ships,
                                 list_of_ships_coordinates))

        # print the game board
        while self.__ships:
            self.__play_one_round()

        # When all ship were destroyed
        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
