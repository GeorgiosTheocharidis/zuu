"""Implements the Player class."""

import sys

import impl.exceptions as exceptions
import impl.room as room

# Aliases.
CommandCannotBeExecuted = exceptions.CommandCannotBeExecuted
ThePlayerWonTheGame = exceptions.ThePlayerWonTheGame
Direction = room.Direction
FailedToExecuteAction = exceptions.FailedToExecuteAction
UnsupportedCommand = exceptions.UnsupportedCommand


class UserCommand:
    """Decorates a member method converting it to a user-command.

    :ivar callable _function: The callable to decorate.
    """

    def __init__(self, function):
        """Initializer.

        :param callable function: The member method to decorate.
        """
        self._function = function

    def __call__(self, the_instance, *args, **kwargs):
        """Allows for callable like behaviour.

        :param Player the_instance: The player instance where the function
        is defined.

        :param args: The args passed to the function.
        :param kwargs: The key-value pairs passed to the function.

        :return: Returns the return value of the wrapped function.
        :rtype: str.
        """
        return str(self._function(the_instance, *args, **kwargs))


class PlayerMeta(type):
    """Used to add the user commands to a Player class. """

    def __init__(cls, name, bases, attrs):
        """Initializes the class.

        :param str name: The name of the class.
        :param tuple bases: The base classes.
        :param dict attrs: The attributes list.
        """
        super().__init__(name, bases, attrs)
        cls._commands = {}
        for base in bases:
            if hasattr(base, '_commands'):
                cls._commands = {**cls._commands, **base._commands}

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, UserCommand):
                cls._commands[attr_name] = attr_value


class Player(metaclass=PlayerMeta):
    """The base class for a player. 
    
    Allows the definition of commands as you specialize its functionality.

    :cvar dict _DIRECTIONS: Used in the "move" command.
    
    :ivar World _word: The world where the player plays.

    :ivar Room _room: The current room where the player stands.

    :ivar set _rooms_already_visited: Holds a list of the room names that
    were already visited.

    :ivar list _bag: Holds collected items from rooms.

    :cvar dict _commands: Holds a list of all the available commands.
    """
    _DIRECTIONS = {
        'up': Direction.NORTH,
        'down': Direction.SOUTH,
        'left': Direction.WEST,
        'right': Direction.EAST,
    }

    _world = None
    _room = None
    _commands = None
    _rooms_already_visited = None
    _bag = None

    def __init__(self, world=None, start_room=None):
        """Initializer.
        
        :param World world: The word to bind.
        :param str start_room: The starting room name.
        """
        self.bind_world(world, start_room)
        self._rooms_already_visited = {
            str(self._room)
        }
        self._bag = []

    def add_to_bag(self, item):
        """Adds a collected item to the bag.

        :param str item: The item to add in the bag.
        """
        self._bag.append(item)

    def is_in_bag(self, item):
        """Checks if an item is in the bag.

        :param str item: The item to check

        :return: True if the item is in the bag.
        :rtype bool.
        """
        return item in self._bag

    def has_already_visited(self, *room_names):
        """Returns true if the player has already visited all the rooms.

        :param *room_names: The room names that the user must have already
        visited.

        :returns: True if the user has already visited all the rooms.
        :rtype: bool.
        """
        for room_name in room_names:
            if room_name not in self._rooms_already_visited:
                return False
        return True

    def bind_world(self, world, room):
        """Binds a world.

        :param World world: The word to bind.
        :param str room: The starting room name.
        """
        self._world = world
        self._room = world.get_room(room)

    def have_won(self):
        """Checks if the player has won the game.

        To be re-implemented in derived Player classes.

        :return: True if the player has won the game.
        :rtype: bool.
        """
        raise NotImplemented

    @property
    def current_room(self):
        """Returns the current room where the player stands.

        :return: The current room where the player stands.
        :type: Room.
        """
        return self._room

    def execute_user_command(self, user_input):
        """Executes a command as it is provided from the user.

        :param str user_input: The space delimited command and arguments
        to execute.

        The first token is the command name and the rest consists of the
        arguments to be passed to the action.

        :return: The return value of the action. This must be a boolean; if
        True this will signify the end of a game.

        :rtype: bool.

        :raises: UnsupportedCommand, FailedToExecuteAction.
        """
        command_name, args = self.unwrap_user_input(user_input)
        command = self._get_command(command_name)
        try:
            return str(command(self, *args))
        except CommandCannotBeExecuted:
            msg = "Command <{}> cannot be executed.".format(user_input)
            raise FailedToExecuteAction(msg)
        except TypeError:
            raise FailedToExecuteAction(
                "Failed to execute: {} ".format(user_input)
            )

    def _get_command(self, command_name):
        """Returns the callable for the specified command.

        :param str command_name: The name of the command to look-up.

        :return: The callable for the passed-in command name.
        :rtype: callable.

        :raises: UnsupportedCommand.
        """
        try:
            return self._commands[command_name]
        except KeyError:
            raise UnsupportedCommand(
                "Command: {} not supported".format(command_name)
            )

    @classmethod
    def unwrap_user_input(cls, user_input):
        """Unwraps the user input.

        :param str user_input: The space delimited command and arguments
        to execute.

        :return: A tuple consisting of the command name and the list of
        arguments.
        """
        tokens = [token for token in user_input.split(' ') if token]
        return tokens[0], tokens[1:]

    @UserCommand
    def move(self, direction):
        """Moves to a direction.
        
        :raises CommandCannotBeExecuted.
        """
        direction = self._DIRECTIONS[direction]
        new_room = self._room.get_neighbor(direction)
        if new_room:
            self._room = new_room
            self._rooms_already_visited.add(str(self._room))
            self._room.update_player(self)
            if self.have_won():
                raise ThePlayerWonTheGame
            return "You are now in: {} ".format(str(self._room))
        else:
            raise CommandCannotBeExecuted

    @UserCommand
    def quit(self):
        """Quits the game exiting the application."""
        sys.exit(0)

    @UserCommand
    def ls(self):
        """lists the available commands."""
        command_names = list(self._commands.keys())
        return 'Available commands: {}'.format(' '.join(command_names))

    @UserCommand
    def where(self):
        """Informs the user of where he currently is.

        :raises CommandCannotBeExecuted.
        """
        msg = "Currently room: <{}>. \n" \
              "Available neighbors: {} \n" \
              "You have already visited: {}".format(
            str(self._room),
            ' '.join(self._room.neighoring_directions),
            ' '.join(['<{}>'.format(room_name) for room_name in
                      self._rooms_already_visited])
        )
        return msg
