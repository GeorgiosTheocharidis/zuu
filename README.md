# zuu
Implements a framework for a simple adventure game.

# Summary

The game consists of a "world" which holds a list of connected rooms. Each room
can have up to four adjacent rooms (also mentioned in the code as neighbors).

The player can navigate the world from room to room going in the four directions
of Up - Down - East - West.  

The objective of the game can be decided dynamically and depends on the story
that is implemented.

# Implementation

#### World

A **World** is an instance of the World class and contains rooms that must be 
created using the command add_room. 

Rooms can be connected using the **connect_rooms** method of the world as can 
be seen in the following example:

    the_world = World()

    name = 'theater'
    description = "lecture theater"
    the_world.add_room(name, description)

    name = 'pub'
    description = "pub"
    the_world.add_room(name, description)

    the_world.connect_rooms('theater', 'pub', Direction.NORTH)
      
Here, we are creating a world, add a couple of rooms and then connect them
using the Direction enumeration that represents the direction from the
first to the second room. Note that to refer to a room we are using
its name. 

#### Player

A player must be an instance of a class that we derive from the **Player**
base class which holds the generic functionality shared among all the types
of games that we want to create.  The derived class must specify the special
behaviour of the player based on the specific game.

An example of this class you can see here:

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
 
Here, we define a player that wins the game is has already visited the
exam_room and the mentoring-room and also has collected the textbook.

When navigating a world the player object is automatically assigned with
the rooms that were already visited which can be checked from the
has_already_visited method.

To specialize behaviour and add items to a bag, we must create a special
type of a Room as it can be seen in this example:

    class RestaurantRoom(Room):
    """Specializes the Room."""

        def update_player(self, the_player):
            """Adds the textbool to the player's bag.
    
            :param Player the_player: The player to update.
            :return:
            """
            the_player.add_to_bag('textbook')
     

In this case each time a RestaurantRoom will be visited the 'textbook' item
will automatically be added to his "bag" so with will become available to
check the winning condition.  To use such a "special" type of a room
you must use code that looks like the following:

    name = 'restaurant'
    description = "restaurant"
    the_world.add_room(name, description, RestaurantRoom)

Note that the Room derived class is passed as a parameter to the add_room.

To create a player you must provide the word and the starting room as 
can be seen here:

    the_player = DummyPlayer(world=the_world, start_room=the_room)

#### Game

And to create a game and run it you can write code similar to this:

    the_game = Game(
        input_reader=read_from_stdio,
        output_writer=write_to_stdio,
        the_player=the_player
    )
    the_game.play()



# How to play
A dummy game that shows how to play can be found under impl/dummygame. Running
this program will put you in command mode:
    > 
    
The build-in commands are:

#### ls

Shows the available commands:

    > ls
    Available commands: where ls quit move
    >
     

#### where

Shows navigation information. 

    > where
    Currently room: <lecture theater>. 
    Available neighbors: up right 
    You have already visited: <lecture theater>
    >
 
#### move <direction>

Allows for navigation. The direction can be up - down - left - right

    > move up
    You are now in: pub 

#### quit

Exits the application.

You are now in: pub
 
    > quit

    Process finished with exit code 0

When you reach the goal of the game the message "You won!" is printed and
the application exits:

    /usr/bin/python3.5 /home/john/samples/zuu/impl/dummygame.py
    > move right
    You won!

To better understand how to play you can use either the dummygame or the
mentoring programs.

#### Creating a new type of a game 

The following are the required steps to create a new type of a game (as 
an example you can use the mentoring.py program.):

* Create your player class deriving from Player and implement the **have_won**
method to reflect the logic of your game.
 
* If you have the need for a custom "command" that is only applicable to your
game you can use the UserCommand decorator similarly to the following: 



    class MyPlayer(Player):
        
        @UserCommand
        def do_something(self, param):
            """Does something.
            
            :param str param: Some param.
            """
            return str(param)
            
Doing so will make the new command available to the game and it will be 
printed when the used asks for help and be executed when the user calls it.        

     
