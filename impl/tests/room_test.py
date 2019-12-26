"""Tests the Room class."""

import unittest

import impl.room as room

# Aliases.
Direction = room.Direction
Room = room.Room


class RoomTest(unittest.TestCase):
    """Tests the Room class."""

    def test_creation(self):
        """Tests the creation of a Room"""
        room_name = 'testing'
        room = Room(room_name)
        self.assertEqual(str(room), room_name)

    def test_get_all_neighbors(self):
        """Tests get_all_neighbors."""
        room1 = Room('room1')
        self.assertListEqual(sorted(room1.neighoring_directions), [])

        room2 = Room('room2')
        room1.add_neighbor(Direction.NORTH, room2)

        self.assertIsNotNone(room1.get_neighbor(Direction.NORTH))
        self.assertIsNone(room1.get_neighbor(Direction.SOUTH))
        self.assertIsNone(room1.get_neighbor(Direction.EAST))
        self.assertIsNone(room1.get_neighbor(Direction.WEST))

        self.assertIn(str(Direction.NORTH), room1.neighoring_directions)
        self.assertNotIn(str(Direction.SOUTH), room1.neighoring_directions)
        self.assertNotIn(str(Direction.EAST), room1.neighoring_directions)
        self.assertNotIn(str(Direction.WEST), room1.neighoring_directions)

        room1.remove_neighbor(Direction.NORTH)
        self.assertNotIn(str(Direction.NORTH), room1.neighoring_directions)

        with self.assertRaises(KeyError):
            room1.remove_neighbor(Direction.NORTH)

    def test_opposite_direction(self):
        """Tests the opposite direction."""
        self.assertEqual(
            Direction.NORTH.get_opposite_direction(), Direction.SOUTH
        )
        self.assertEqual(
            Direction.SOUTH.get_opposite_direction(), Direction.NORTH
        )
        self.assertEqual(
            Direction.WEST.get_opposite_direction(), Direction.EAST
        )
        self.assertEqual(
            Direction.EAST.get_opposite_direction(), Direction.WEST
        )
        

if __name__ == '__main__':
    unittest.main()
