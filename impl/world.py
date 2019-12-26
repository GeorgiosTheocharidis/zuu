"""Implements a world consisting of rooms."""

import impl.exceptions as exceptions
import impl.room as room

# Aliases.
Direction = room.Direction
Room = room.Room
RoomAlreadyExists = exceptions.RoomAlreadyExists
RoomDoesNotExist = exceptions.RoomDoesNotExist


class World:
    def __init__(self):
        self._rooms = {}

    def add_room(self, name, description, room_class=None):
        """Adds a room.

        :param str name: The name of the room.
        :param str description: The description of the room.

        :param Room room_class: A Room derived class in case you need to
        specialize the room construction.

        :raises: RoomAlreadyExists.
        """
        if name in self._rooms:
            raise RoomAlreadyExists(
                "Room {} already exists.".format(name)
            )
        room_class = room_class or Room
        self._rooms[name] = room_class(description)

    def get_room(self, name):
        """Gets a room by its name.

        :param str name: The name of the room.

        :returns: The room for the passed-in name.
        :rtype: Room.

        :raises: RoomDoesNotExist.
        """
        try:
            return self._rooms[name]
        except KeyError:
            raise RoomDoesNotExist("Room {} does not exist.".format(name))

    def connect_rooms(self, room_name_1, room_name_2, direction):
        """Connects two rooms.

        :param str room_name_1: The name of the room to connect.
        :param str room_name_2: The name of the room to be connected.
        :param Direction direction: The direction to connect.

        :raises: RoomDoesNotExist.
        """
        room1 = self.get_room(room_name_1)
        room2 = self.get_room(room_name_2)
        room1.add_neighbor(direction, room2)
        room2.add_neighbor(direction.get_opposite_direction(), room1)
