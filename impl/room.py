"""Implements the Room class."""

import enum


class Direction(enum.Enum):
    """Represents the available directions.

    :cvar int NORTH: Go north.
    :cvar int SOUTH: Go south.
    :cvar int WEST: Go west.
    :cvar int EAST: Go east.
    """

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def get_opposite_direction(self):
        """Returns the opposite direction.

        :return: The opposite direction.
        :rtype: Direction.
        """
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.WEST:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.WEST

    def __str__(self):
        """Converts a direction to human friendly representation."""
        if self == Direction.NORTH:
            return 'up'
        elif self == Direction.SOUTH:
            return 'down'
        elif self == Direction.EAST:
            return 'right'
        elif self == Direction.WEST:
            return 'left'


class Room:
    """ A "Room" represents one location in the scenery of the game.

    It is connected to other rooms via exits.  For each existing exit, the room
    stores a reference to the neighboring room.

    :ivar str _description: The description of the room.
    :ivar dict _adjacent_rooms: The adjacent rooms
    """

    def __init__(self, description):
        """ Create a room described "description".
        
        :param str description: The description of the room.
        """
        self._description = description
        self._adjacent_rooms = {}

    def add_neighbor(self, direction, adjacent_room):
        """ Define an adjacent_room.

        :param Direction direction: The direction of the adjacent_room.
        :param Room adjacent_room: The adjacent_room.
        """
        self._adjacent_rooms[direction] = adjacent_room

    def remove_neighbor(self, direction):
        """Removes an adjacent_room.

        :param Direction direction: The direction of the adjacent_room.

        :raises: KeyError.
        """
        del self._adjacent_rooms[direction]

    def update_player(self, the_player):
        """Updates the status of the player based on room specifics.

        Currently does nothing but you can implement this functionality
        in derived classes to fit your game needs.

        :param Player the_player: The player to update.
        :return:
        """

    def __str__(self):
        """ Returns The short description of the room."""
        return self._description

    @property
    def neighoring_directions(self):
        """ Return a string describing all the neighoring_directions.
        
        Example:
        "Exits: north west".

        :returns: Details of the room's exits.
        :rtype: str.
        """
        return [str(direction) for direction in self._adjacent_rooms.keys()]
        
    def get_neighbor(self, direction):
        """Gets neighbor room by directiion. 
        
        If there is no room in that direction, return None.

        :param Direction direction: The neighbor's direction.
            
        :returns:  The room in the given direction.
        :rtype: Room.
        """
        return self._adjacent_rooms.get(direction)
