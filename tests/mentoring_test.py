"""Tests the mentoring game."""

import unittest

import impl.exceptions as exceptions
import impl.game as game
import mentoring

ThePlayerWonTheGame = exceptions.ThePlayerWonTheGame

# Specifies a command sequence that wins the game.
_WINNING_COMMAND_SEQUENCE = [
    'ls',
    'where',
    'move down',
    'move up',
    'where',
    'move right',
    'move down',
    'move left',
    'move down',
    'move left',
    'move up',
    'move right',
    'where',
]


def make_reader(lines):
    """Reads user input from the standard input.

    :return: The user input.
    :rtype: str.
    """
    index = 0

    def reader():
        """Simulates the user input.

        :return: A string simulating user input.
        :rtype: str.
        """
        nonlocal index
        if index > len(lines):
            raise IndexError
        line = lines[index]
        index += 1
        return line

    return reader


def make_writer(output_strings):
    """Makes a predictable writer to allow us to test the output.

    :param list output_strings: The list that will receive the output.
    """

    def writer(msg):
        """Writes a message to the output list.

        :param str msg: The string to write.
        """
        output_strings.append(msg)

    return writer


class NoExitGame(mentoring.Game):
    """Overloads the exit method to allow smooth testing."""

    def exit(self):
        """Exits the application."""


class MentoringTest(unittest.TestCase):
    """Tests the mentoring game.

    :param list output_strings: Holds the output for each run.
    """

    def setUp(self):
        """Sets up the necessary objects."""

        self.output_strings = []
        the_world, the_room = mentoring.make_the_world()

        the_player = mentoring.MentoringPlayer(world=the_world,
                                               start_room=the_room)

        self.the_game = NoExitGame(
            input_reader=make_reader(_WINNING_COMMAND_SEQUENCE),
            output_writer=make_writer(self.output_strings),
            the_player=the_player
        )

    def test_winning_the_game(self):
        """Tests winning the game."""
        self.the_game.play()
        self.assertEqual(game.WINNING_MSG, self.output_strings[-1])


if __name__ == '__main__':
    unittest.main()
