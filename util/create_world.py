from django.contrib.auth.models import User
from adventure.models import Player, Room
import random


Room.objects.all().delete()
# World.objects.all().delete()


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x
        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        # While there are rooms to be created...
        previous_room = None
        #switch out while loop for a for loop...
        #for i in range(1, 100):
        while room_count < num_rooms:
            print("room count", room_count)
            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                print("if", x)
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                print("elif", x)
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                print("else", x)
                room_direction = "n"
                y += 1
                direction *= -1
            # Create a room in the given direction
            name_adj = ["dark", "cold", "warm",
                        "bright", "damp", "smelly", "dry"]
            place_noun = ["corridor", "room", "cave", "nook",
                          "ampitheater", "alcove", "passageway"]
            desc_verb = ["enter", "cross the threshold of", "gain access to",
                         "set foot in", "crawl into", "approach", "run into", "pass into"]
            desc_sight = ["a panda", "a pile of gold", "a pot roast",
                          "Darth Vader", "a velociraptor", "Dora the Explorer"]
            desc_sense = ["see", "hear", "smell",
                          "feel", "sense the presence of"]
            desc_location = ["Overhead", "Beneath your feet",
                             "To the right", "To the left", "Behind you", "Ahead of you"]
            # so you get the same location in both the title and the description
            noun = random.choice(place_noun)
            # title
            adjective = random.choice(name_adj)
            #print(f"{adjective} {noun}")
            # description
            movement_verb = random.choice(desc_verb)
            location = random.choice(desc_location)
            sense = random.choice(desc_sense)
            sight = random.choice(desc_sight)
            # verb######place###where##########sense####thing
            # You _enter_ a _room_. _Overhead_, you _see_ a _thing_.""
            #print(f"You {movement_verb} a {noun}. {location}, you {sense} {sight}")
            room = Room(room_count, adjective + " " + noun,
                        "You " + movement_verb + " a " + noun + ". " + location + " you " + sense + " " + sight, x, y)
            room.save()
            print("room", room)
            # Note that in Django, you'll need to save the room after you create it
            # Save the room in the World grid
            self.grid[y][x] = room
            print("gridroom", room)
            # Connect the new room to the previous room
            if previous_room is not None:
                print("previous room", previous_room)
                print("room in connect", room)
                print("room_dir", room_direction)
                previous_room.connectRooms(room, room_direction)
            # Update iteration variables
            previous_room = room
            room_count += 1

# name generator

# r_outside = Room(title="Outside Cave Entrance",
#                description="North of you, the cave mount beckons")

# r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
# passages run north and east.""")

# r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
# into the darkness. Ahead to the north, a light flickers in
# the distance, but there is no way across the chasm.""")

# r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
# to north. The smell of gold permeates the air.""")

# r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
# chamber! Sadly, it has already been completely emptied by
# earlier adventurers. The only exit is to the south.""")
# r_{name}.save()
# r_outside.save()
# r_foyer.save()
# r_overlook.save()
# r_narrow.save()
# r_treasure.save()

# Link rooms together
# r_outside.connectRooms(r_foyer, "n")
# r_foyer.connectRooms(r_outside, "s")

# r_foyer.connectRooms(r_overlook, "n")
# r_overlook.connectRooms(r_foyer, "s")

# r_foyer.connectRooms(r_narrow, "e")
# r_narrow.connectRooms(r_foyer, "w")

# r_narrow.connectRooms(r_treasure, "n")
# r_treasure.connectRooms(r_narrow, "s")

# players=Player.objects.all()
# for p in players:
#   p.currentRoom=r_outside.id
#   p.save()

# createWorld()



w = World()
number_of_rooms = 100
width = 20
height = 20
w.generate_rooms(width, height, number_of_rooms)
