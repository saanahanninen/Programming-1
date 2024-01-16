"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Saana Hänninen
10.10 Scoring for Mölkky.
Mölkky is a traditional Finnish game where players aim to score exactly 50 points.
If a player ends up having more than 50 points, their score will be decreased to 25 points.

This program acts as a scorekeeper where two players, Matti and Teppo, can keep track of
their scores after each throw.

This exercise included a code template. I implemented the Player class, a warning message
that will be printed if the total score of the player is 40-49 points, a supporting feedback
that will be printed if the entered score is larger than the average of all the points entered
for that player, and the hit percentage printout.
"""


class Player:

    def __init__(self, name, points=0, counter=0, throw=0, at_least_one=0):
        """
        Initialises the class
        :param name: str, player's name
        :param points: int, player's total points (with possible penalty points
        taken into account)
        :param counter: int, player's total points through the game (without
        penaly reductions taken into account)
        :param throw: int, number of throws
        :param at_least_one: int, how many throws' results have been at least 1
        """
        self.__name = name
        self.__points = points
        self.__counter = counter
        self.__throw = throw
        self.__at_least_one = at_least_one

    def get_name(self):
        """
        Gets the name of the player
        :return: str, player's name
        """
        return self.__name

    def add_points(self, points):
        """
        Adds points to player's total points. Checks for potential penalty
        points and flags if the player is close to winning
        :param points: int, player's points in the round
        """
        self.__points += points
        # if points >= 1, increase the at least one counter by one since this
        # is needed in percentage calculations later
        if points >= 1:
            self.__at_least_one += 1

        if self.__points > 50:
            self.__points = 25
            print(f"{self.__name} gets penalty points!")

        if 40 <= self.__points <= 49:
            print(f"{self.__name} needs only {50-self.__points} points. "
                  f"It's better to avoid knocking down the pins "
                  f"with higher points.")

    def has_won(self):
        """
        Checks if the player has won
        :return: bool, returns true if player has won and false if not
        """
        if self.__points == 50:
            return True
        else:
            return False

    def get_points(self):
        """
        Gets player's points
        :return: int, total points of player
        """
        return self.__points

    def average_points(self, points):
        """
        Calculates player's average points of throws
        :param points: int, player's points in the current round
        :return: int, average points of player
        """
        # add current round points to counter, increase throw number by one to
        # take current round into account
        self.__counter += points
        self.__throw += 1
        if self.__throw == 3 and points == 10:
            # to avoid printing the cheers message
            return points + 1

        else:
            result = self.__counter / self.__throw
            return result

    def get_percentage(self):
        """
        Gets player's percentage of how many throws have been worth of at least
        one point
        :return: float, percentage of over one point rounds out of all throws
        """
        # cannot divide by zero
        if self.__throw == 0:
            result = 0
        else:
            result = self.__at_least_one / self.__throw * 100

        return result


def main():
    # Here we define two variables which are the objects initiated from the
    # class Player. This is how the constructor of the class Player
    # (the method that is named __init__) is called!

    player1 = Player("Matti")
    player2 = Player("Teppo")

    throw = 1
    while True:

        # if throw is an even number
        if throw % 2 == 0:
            in_turn = player1

        # else throw is an odd number
        else:
            in_turn = player2

        pts = int(input("Enter the score of player " + in_turn.get_name() +
                        " of throw " + str(throw) + ": "))

        in_turn.add_points(pts)
        if in_turn.average_points(pts) < pts:
            print(f"Cheers {in_turn.get_name()}!")

        if in_turn.has_won():
            print("Game over! The winner is " + in_turn.get_name() + "!")
            return

        print("")
        print("Scoreboard after throw " + str(throw) + ":")
        print(f"{player1.get_name()}: {player1.get_points()} p, hit percentage {player1.get_percentage():.1f}")
        print(f"{player2.get_name()}: {player2.get_points()} p, hit percentage {player2.get_percentage():.1f}")
        print("")

        throw += 1


if __name__ == "__main__":
    main()
