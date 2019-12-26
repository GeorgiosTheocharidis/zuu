"""Tests the Word class."""

import unittest

import impl.world as world

# Aliases.
Direction = world.Direction
Room = world.Room
World = world.World


class WorldTest(unittest.TestCase):
    """Tests the Word class."""

    def test_add_room(self):
        """Tests the add_room method."""
        the_world = World()
        name = 'theater'
        description = "in a lecture theater"
        the_world.add_room(name, description)
        r = the_world.get_room(name)
        self.assertEqual(str(r), description)

    def test_connect_rooms(self):
        """Tests connecting two rooms."""
        the_world = World()

        name = 'theater'
        description = "in a lecture theater"
        the_world.add_room(name, description)

        name = 'pub'
        description = "in the campus pub"
        the_world.add_room(name, description)

        the_world.connect_rooms('theater', 'pub', Direction.NORTH)

        theater = the_world.get_room('theater')
        pub = the_world.get_room('pub')

        self.assertIs(theater, pub.get_neighbor(Direction.SOUTH))
        self.assertIs(pub, theater.get_neighbor(Direction.NORTH))
        

if __name__ == '__main__':
    unittest.main()
