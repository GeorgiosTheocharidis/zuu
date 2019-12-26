"""Implements the first example of the exercise."""

import impl.game as game
import impl.player as player
import impl.room as room
import impl.world as world

# Aliases.
Direction = room.Direction
Game = game.Game
Player = player.Player
World = world.World
Room = room.Room


class MentoringPlayer(Player):
    """Specializes the Player class for the mentoring game."""

    def have_won(self):
        """Checks if the player has won the game.

        To be re-implemented in derived Player classes.

        :return: True if the player has won the game.
        :rtype: bool.
        """
        if not self.has_already_visited('exam_room', 'mentoring-room'):
            return False

        return self.is_in_bag('textbook')


class RestaurantRoom(Room):
    """Specializes the Room."""

    def update_player(self, the_player):
        """Adds the textbool to the player's bag.

        :param Player the_player: The player to update.
        :return:
        """
        the_player.add_to_bag('textbook')


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

    name = 'restaurant'
    description = "restaurant"
    the_world.add_room(name, description, RestaurantRoom)

    name = 'engineering_reception'
    description = "Engineering Reception"
    the_world.add_room(name, description)

    name = 'exam_room'
    description = "exam_room"
    the_world.add_room(name, description)

    name = 'class_room1'
    description = "class_room1"
    the_world.add_room(name, description)

    name = 'class_room2'
    description = "class_room2"
    the_world.add_room(name, description)

    name = 'mentoring-room'
    description = "mentoring-room"
    the_world.add_room(name, description)

    the_world.connect_rooms('theater', 'pub', Direction.NORTH)
    the_world.connect_rooms('theater', 'mentoring-room', Direction.EAST)

    the_world.connect_rooms('theater', 'restaurant', Direction.SOUTH)
    the_world.connect_rooms('restaurant', 'class_room1', Direction.EAST)
    the_world.connect_rooms('restaurant', 'class_room2', Direction.WEST)

    the_world.connect_rooms('class_room2',
                            'engineering_reception', Direction.NORTH)

    the_world.connect_rooms('engineering_reception', 'exam_room',
                            Direction.EAST)

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

    the_player = MentoringPlayer(world=the_world, start_room=the_room)

    the_game = Game(
        input_reader=read_from_stdio,
        output_writer=write_to_stdio,
        the_player=the_player
    )
    the_game.play()


if __name__ == '__main__':
    main()
