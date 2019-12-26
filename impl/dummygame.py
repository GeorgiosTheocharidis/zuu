"""Implements a dummy game that you use for testing."""

import impl.game as game
import impl.player as player
import impl.room as room
import impl.world as world

# Aliases.
Direction = room.Direction
Game = game.Game
Player = player.Player
World = world.World


class DummyPlayer(Player):
    """Implements a dummy player."""

    def have_won(self):
        """Checks if the player has won the game.

        To be re-implemented in derived Player classes.

        :return: True if the player has won the game.
        :rtype: bool.
        """
        return self.has_already_visited('classroom1')


def make_the_world():
    """Makes a world.

    :return: A tuple consisting of the world and the first room.
    :rtype: tuple.
    """
    the_world = World()

    name = 'theater'
    description = "lecture theater"
    the_world.add_room(name, description)

    name = 'pub'
    description = "pub"
    the_world.add_room(name, description)

    name = 'classroom1'
    description = "classroom1"
    the_world.add_room(name, description)

    the_world.connect_rooms('theater', 'pub', Direction.NORTH)
    the_world.connect_rooms('theater', 'classroom1', Direction.EAST)
    return the_world, 'theater'


def read_from_stdio():
    """Reads user input from the standard input.
    
    :return: The user input.
    :rtype: str.
    """
    return input("> ")


def write_to_stdio(msg):
    """Writes a message to the standard output.

    :param str msg: The string to write.
    """
    print(msg)


def main():
    """Runs a game."""
    the_world, the_room = make_the_world()

    the_player = DummyPlayer(world=the_world, start_room=the_room)

    the_game = Game(
        input_reader=read_from_stdio,
        output_writer=write_to_stdio,
        the_player=the_player
    )
    the_game.play()


if __name__ == '__main__':
    main()
