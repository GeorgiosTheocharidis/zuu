"""Runs a game."""

import sys

import impl.room as room
import impl.exceptions as exceptions

# Aliases.
Direction = room.Direction
ThePlayerWonTheGame = exceptions.ThePlayerWonTheGame
ZuulException = exceptions.ZuulException

# The message to signify a win.
WINNING_MSG = 'You won!'

class Game:
    """Represents a generic Game.

    :ivar callable _input_reader: Callable to read the user input. Must be
    function receiving no arguments are returning a string representing the
    user's input.

    :ivar callable _output_writer: Callable to write to output. Used to
    communicate with the user. Must be a callable receiving a single argument.

    :ivar Player _the_player: The instance of the Player.
    """

    _input_reader = None
    _output_writer = None
    _the_player = None

    def __init__(self,
                 input_reader=None,
                 output_writer=None,
                 the_player=None):
        """Initializer.
        
        :param callable input_reader: Callable to read the user input.

        :param callable output_writer: Callable to write to output. Used to
        communicate with the user. Must be a callable receiving
        a single argument.

        :param Player the_player: The instance of the player to use.
        """
        self.bind_input_reader(input_reader)
        self.bind_output_writer(output_writer)
        self.bind_player(the_player)

    def bind_input_reader(self, input_reader):
        """Binds an input reader callable.

        :param callable input_reader: Callable to read the user input.
        """
        assert callable(input_reader)
        self._input_reader = input_reader

    def bind_output_writer(self, output_writer):
        """Binds an output writer callable.

        :param callable output_writer: Callable to write output to.
        """
        assert callable(output_writer)
        self._output_writer = output_writer

    def bind_player(self, the_player):
        """Binds the player.

        :param Player the_player: The player instance to bind.
        """
        self._the_player = the_player

    def exit(self):
        """Exits the application."""
        sys.exit(0)

    def play(self):
        """Plays the game handling user input."""
        assert callable(self._input_reader), \
            "You must provide the input reader."
        assert callable(self._output_writer), \
            "You must provide the input writer."
        assert self._the_player, "You must provide the player."

        while True:
            try:
                user_input = self._input_reader()
                output = self._the_player.execute_user_command(user_input)
            except ThePlayerWonTheGame:
                self._output_writer(WINNING_MSG)
                break
            except ZuulException as ex:
                self._output_writer(str(ex))
            else:
                self._output_writer(output)
        self.exit()
