from screen import Screen
import sys
from ship import *
from asteroid import *
from torpedo import *

SECOND_ASTEROID = 1
SPLIT = 2
DEFAULT_ASTEROIDS_NUM = 5
STARTING_SCORE = 0
MAX_TORPEDOS = 15
SMALLEST_ASTEROID = 1
MEDIUM_ASTEROID = 2
LARGE_ASTEROID = 3
NO_ASTEROID_ON_SCREEN = 0

class GameRunner:
    def __init__(self, asteroids_amnt):
        self._screen = Screen()
        self.__ship = Ship()
        self.asteroids = list(Asteroid() for i in range(asteroids_amnt))
        self.screen_max_x = Screen
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.asteroids_register()
        self.torpedos = list()
        self.register_torpedoes = list()
        self.__score = STARTING_SCORE

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def add_score(self, screen, size):
        if size == SMALLEST_ASTEROID:
            self.__score += 100
        elif size == MEDIUM_ASTEROID:
            self.__score += 50
        elif size == LARGE_ASTEROID:
            self.__score += 20
        screen.set_score(self.__score)

    def split_asteroid(self, screen, asteroid, torpedo):
        for i in range(SPLIT):
            small_asteroid = Asteroid()
            small_asteroid.set_size(asteroid.get_size() - SMALLEST_ASTEROID)
            small_asteroid.set_x_speed(self.smaller_x_asteroid_speed(asteroid, torpedo))
            small_asteroid.set_y_speed(self.smaller_y_asteroid_speed(asteroid, torpedo))
            small_asteroid.set_x_axis_coordinate(asteroid.get_x_axis_coordinate())
            small_asteroid.set_y_axis_coordinate(asteroid.get_y_axis_coordinate())
            if i == SECOND_ASTEROID:
                small_asteroid.set_x_speed(-self.smaller_x_asteroid_speed(asteroid, torpedo))
                small_asteroid.set_y_speed(-self.smaller_y_asteroid_speed(asteroid, torpedo))
            self.asteroids.append(small_asteroid)
            screen.register_asteroid(small_asteroid, small_asteroid.get_size())

    def add_torpedo(self):
        '''this function will create new torpedo and will add him to the list of torpedos'''
        self.torpedos.append(Torpedo(self.__ship.get_x_axis_coordinate(), self.__ship.get_y_axis_coordinate(),
                                     self.__ship.get_x_speed(), self.__ship.get_y_speed(),
                                     self.__ship.get_heading()))

    def add_score_to_screen(self, asteroid):
        self.add_score(self._screen, asteroid.get_size())  # add scores when torpedo hits

    def smaller_x_asteroid_speed(self, asteroid, torpedo):
        new_x_speed = (torpedo.get_x_speed() + asteroid.get_x_speed()) / \
                      (math.sqrt((asteroid.get_x_speed())**2 + (asteroid.get_y_speed())**2))
        return new_x_speed

    def smaller_y_asteroid_speed(self, asteroid, torpedo):
        new_y_speed = (torpedo.get_y_speed() + asteroid.get_y_speed()) / \
                      (math.sqrt((asteroid.get_x_speed())**2 + (asteroid.get_y_speed())**2))
        return new_y_speed

    def check_ship_intersection(self, ship):
        ''' this function will check if an asteroid hit the ship, if true deletes the asteroid and return true'''
        for asteroid in self.asteroids:
            if asteroid.has_intersection(ship):
                # unregister astroid
                self._screen.unregister_asteroid(asteroid)
                self.asteroids.remove(asteroid)
                return True

    def end_game(self):
        '''
        this function will end the game in 3 conditions(also adds a message accordingly):
        1. if all asteroids destroyed
        2. if the ship's health is zero
        3. if the player decides to quit and press q
        '''
        if self.asteroids == NO_ASTEROID_ON_SCREEN:
            self._screen.show_message("YON WON!",
                                      "ALL ASTEROIDS HAVE BLOWN UP")
            return True
        elif self._screen.should_end():
            self._screen.show_message("GOOD BYE!",
                                      "COME BACK LATER!")
            return True

        elif not self._screen._lives:
            self._screen.show_message("LOST!",
                                      "YOU HAVE RAN OUT OF LIFES!")
            return True
        else:
            return False

    def torpedo_intersection(self, torpedo, asteroid):
        '''
        we will call this function when asteroid and torpedo hit. than the function will delete the
         asteroid(accordingly) and will delete the torpedo who hit the asteroid
        :param torpedo: Torpedo object
        :param asteroid: Asteroid object
        :return: None
        '''
        if asteroid.get_size() != SMALLEST_ASTEROID:
            self.split_asteroid(self._screen, asteroid, torpedo)
            self._screen.unregister_asteroid(asteroid)
            self.asteroids.remove(asteroid)
        if asteroid.get_size() == SMALLEST_ASTEROID:
            self._screen.unregister_asteroid(asteroid)
            self.asteroids.remove(asteroid)
        self.torpedos.remove(torpedo)
        self.register_torpedoes.remove(torpedo)
        self._screen.unregister_torpedo(torpedo)

    def _game_loop(self):
        '''
        this function is our main function in the game.
        it will check every detail in the game and will react accordingly
        :return: None
        '''
        if self.end_game():
            self._screen.end_game()
            sys.exit()

        else:
            # draw ship on the screen
            self._screen.draw_ship(self.__ship.get_x_axis_coordinate(), self.__ship.get_y_axis_coordinate(),
                                   self.__ship.get_heading())

            # draw asteroids on the screen
            self.asteroids_draw()

            # move registered asteroids
            self.asteroids_move()

            # move ship
            self.move(self.__ship)

            # Check directions
            if self._screen.is_left_pressed():
                self.__ship.change_direction_left()
            elif self._screen.is_right_pressed():
                self.__ship.change_direction_right()

            # Check acceleration
            if self._screen.is_up_pressed():
                self.__ship.accelerate_ship()

            # Check ship intersection
            if self.check_ship_intersection(self.__ship):
                self._screen.show_message("collision", "be careful!!")
                self._screen.remove_life()

            #moves the torpedos and creats them
            if self._screen.is_space_pressed() and len(self.register_torpedoes) < MAX_TORPEDOS:
                self.add_torpedo()
            for torpedo in self.torpedos:
                if torpedo not in self.register_torpedoes:
                    self._screen.register_torpedo(torpedo)
                    self.register_torpedoes.append(torpedo)
                    #draws torpedo on the screen with his new coords
                self._screen.draw_torpedo(torpedo, torpedo.get_x_axis_coordinate(), torpedo.get_y_axis_coordinate(),
                                          torpedo.get_heading())
                self.move(torpedo)
                torpedo.add_steps()
                #checks if torpedo already did his max steps and reacts accordingly
                if torpedo.get_steps() >= torpedo.max_steps():
                    self.torpedos.remove(torpedo)
                    self.register_torpedoes.remove(torpedo)
                    self._screen.unregister_torpedo(torpedo)
            # end

            #checks intersection with torpedoes, and deletes accordingly, add scores
            for asteroid in self.asteroids:
                for torpedo in self.register_torpedoes:
                    if asteroid.has_intersection(torpedo):
                        self.add_score_to_screen(asteroid)
                        self.torpedo_intersection(torpedo, asteroid)

    def asteroids_register(self):
        for asteroid in self.asteroids:
            self._screen.register_asteroid(asteroid, asteroid.get_size())

    def asteroids_draw(self):
        for asteroid in self.asteroids:
            # draw asteroids on the screen
            self._screen.draw_asteroid(asteroid,
                                       asteroid.get_x_axis_coordinate(),
                                       asteroid.get_y_axis_coordinate())

    def asteroids_move(self):
        for asteroid in self.asteroids:
            self.move(asteroid)


    def move(self,obj):
        """

        :return:
        """
        delta_x = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
        delta_y = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y

        # calculate new location on x axis
        new_x_location = (obj.get_x_speed() +
                          obj.get_x_axis_coordinate() -
                          Screen.SCREEN_MIN_X) % delta_x + \
                          Screen.SCREEN_MIN_X

        # set the new location the field
        obj.set_x_axis_coordinate(new_x_location)

        # calculate new location on y axis
        new_y_location = (obj.get_y_speed() +
                          obj.get_y_axis_coordinate() -
                          Screen.SCREEN_MIN_Y) % delta_y + \
                          Screen.SCREEN_MIN_Y

        # set the new location to field
        obj.set_y_axis_coordinate(new_y_location)


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
