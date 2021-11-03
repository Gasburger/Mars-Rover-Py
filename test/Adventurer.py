class Adventurer:
    def __init__(self):
        """TODO: Initialises an adventurer object."""
        self.inventory = []
        self.skill = 5
        self.will = 5


    def get_inv(self):
        """TODO: Returns the adventurer's inventory."""
        return self.inventory

    def get_skill(self):
        """TODO: Returns the adventurer's skill level. Whether this value is generated before or after item bonuses are applied is your decision to make."""
        return self.skill

    def get_will(self):
        """TODO: Returns the adventurer's will power. Whether this value is generated before or after item bonuses are applied is your decision to make."""
        return self.will

    def take(self, item):
        """TODO: Adds an item to the adventurer's inventory."""
        self.inventory.append(item)

    def check_self(self):
        """TODO: Shows adventurer stats and all item stats."""
        
class Item:
	def __init__(self, name, short, skill_bonus, will_bonus):
		"""TODO: Initialises an item."""
		self.name = name
		self.short = short
		self.skill_bonus = skill_bonus
		self.will_bonus = will_bonus
 
	def get_name(self):
		"""TODO: Returns an item's name."""
		return self.name

	def get_short(self):
		"""TODO: Returns an item's short name."""
		return self.short

	def get_info(self):
		"""TODO: Prints information about the item."""
		print(self.name)
		print("Grants a bonus of", self.skill_bonus, "to SKILL.")
		print("Grants a bonus of", self.will_bonus, "to WILL.")

	def get_skill(self):
		"""TODO: Returns the item's skill bonus."""
		return self.skill_bonus

	def get_will(self):
		"""TODO: Returns the item's will bonus."""
		return self.will_bonus
		

class Quest:
	def __init__(self, reward, action, desc, before, after, req, fail_msg, pass_msg, room):
		"""TODO: Initialises a quest."""
		self.reward = reward
		self.action = action
		self.desc = desc
		self.before = before
		self.after = after
		self.req = req
		self.fail_msg = fail_msg
		self.pass_msg = pass_msg
		self.room = room

	def get_info(self):
		"""TODO: Returns the quest's description."""
		...

	def is_complete(self):
		"""TODO: Returns whether or not the quest is complete."""
		

	def get_action(self):
		"""TODO: Returns a command that the user can input to attempt the quest."""
		...

	def get_room_desc(self):
		"""TODO: Returns a description for the room that the quest is currently in. Note that this is different depending on whether or not the quest has been completed."""
		...

	def attempt(self, player):
		"""TODO: Allows the player to attempt this quest.

		Check the cumulative skill or will power of the player and all their items. If this value is larger than the required skill or will threshold for this quest's completion, they succeed and are rewarded with an item (the room's description will also change because of this).

		Otherwise, nothing happens."""
		...

class Room:
	def __init__(self, name):
		"""TODO: Initialises a room. Do not change the function signature (line 2)."""
		self.name = name
		
	def get_name(self):
		"""TODO: Returns the room's name."""
		return self.name

	def get_short_desc(self):
		"""TODO: Returns a string containing a short description of the room. This description changes based on whether or not a relevant quest has been completed in this room.

		If there are no quests that are relevant to this room, this should return: 'There is nothing in this room.' """
		

	def get_quest_action(self):
		"""TODO: If a quest can be completed in this room, returns a command that the user can input to attempt the quest."""
		...

	def set_quest(self, q):
		"""TODO: Sets a new quest for this room."""
		...

	def get_quest(self):
		"""TODO: Returns a Quest object that can be completed in this room."""
		...
		
	def set_path(self, dir, dest):
		"""TODO: Creates an path leading from this room to another."""
		

	def draw(self, north, south, east, west):
		self.north = north
		self.south = south
		self.east = east
		self.west = west
		"""TODO: Creates a drawing depicting the exits in each room."""
		print("")
		if self.north == None:
			print("+--------------------+")
		else:
			print("+---------NN---------+")
		if self.west == None and self.east == None:
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
		elif self.west == None and self.east != None:
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    E")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
		elif self.west != None and self.east == None:
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("W                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
		else:
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("W                    E")
			print("|                    |")
			print("|                    |")
			print("|                    |")
			print("|                    |")
		if self.south == None:
			print("+--------------------+")
		else:
			print("+---------SS---------+")

		print("You are standing at the " + self.name + ".")
		print("")


	def move(self, dir):
		"""TODO: Returns an adjoining Room object based on a direction given. (i.e. if dir == "NORTH", returns a Room object in the north)."""
		...

from room import Room
from item import Item
from adventurer import Adventurer
from quest import Quest
import sys


def read_paths(source):
	"""Returns a list of lists according to the specifications in a config file, (source).

	source contains path specifications of the form:
	origin > direction > destination.

	read_paths() interprets each line as a list with three elements, containing exactly those attributes. Each list is then added to a larger list, `paths`, which is returned."""

	# TODO

	source = sys.argv[1]
	paths = []

	f = open(source, "r")
	f1 = f.readlines()

	if len(f1) == 0:
		print("No rooms exist! Exiting program...")
		sys.exit()
	else:
		for x in f1:
			c = x.strip()
			c = c.split(" > ")
			paths.append(c)
		return paths
		f.close()


def create_rooms(paths):
	"""Receives a list of paths and returns a list of rooms based on those paths. Each room will be generated in the order that they are found."""

	# TODO
	rooms = []

	paths = read_paths(sys.argv[1])

	for x in range(0, len(paths)):
		for j in range(0, 3):
			if paths[x][j] != "NORTH" and paths[x][j] != "SOUTH" and paths[x][j] != "EAST" and paths[x][j] != "WEST":
				rooms.append(paths[x][j])
			else:
				pass

	rooms = list(dict.fromkeys(rooms))
	return rooms


def generate_items(source):
	"""Returns a list of items according to the specifications in a config file, (source).

	source contains item specifications of the form:
	item name | shortname | skill bonus | will bonus
	"""

	# TODO

	source = sys.argv[2]
	items = []

	f = open(source, "r")
	f1 = f.readlines()

	
	for x in f1:
		c = x.strip()
		c = c.split(" | ")
		items.append(c)
	return items
	f.close()


def generate_quests(source, items, rooms):
	"""Returns a list of quests according to the specifications in a config file, (source).

	source contains quest specifications of the form:
	reward | action | quest description | before_text | after_text | quest requirements | failure message | success message | quest location
	"""
	
	# TODO

	source = sys.argv[3]
	quests = []

	f = open(source, "r")
	f1 = f.readlines()

	
	for x in f1:
		c = x.strip()
		c = c.split(" | ")
		quests.append(c)
		quests.remove("")
	return quests
	f.close()

	


# TODO: Retrieve info from CONFIG files. Use this information to make Adventurer, Item, Quest, and Room objects.

if len(sys.argv) < 4:
	print("Usage: python3 simulation.py <paths> <items> <quests>")
	sys.exit()

try:
	open_paths = open(sys.argv[1], "r")
	open_items = open(sys.argv[2], "r")
	open_quests = open(sys.argv[3], "r")

	open_paths.close()
	open_items.close()
	open_quests.close()

except FileNotFoundError:
	print("Please specify a valid configuration file.")
	sys.exit()

# TODO: Receive commands from standard input and act appropriately.




paths = read_paths(sys.argv[1])
room_name = paths[0][0]
current_room = room_name

if paths[0][1] == "NORTH":
	north = True
	south = None
	east = None
	west = None
elif paths[0][1] == "SOUTH":
	south = True
	north = None
	east = None
	west = None
elif paths[0][1] == "EAST":
	east = True
	south = None
	north = None
	west = None
elif paths[0][1] == "WEST":
	west = True
	east = None
	south = None
	north = None
else:
	pass

Room(room_name).draw(north, south, east, west)

while True:
	x = input(">>> ").upper()
	
	if x == "QUIT":
		print("Bye!")
		sys.exit()

	elif x == "HELP":
		print("HELP       - Shows some available commands.")
		print("LOOK or L  - Lets you see the map/room again.")
		print("QUESTS     - Lists all your active and completed quests.")
		print("INV        - Lists all the items in your inventory.")
		print("CHECK      - Lets you see an item (or yourself) in more detail.")
		print("NORTH or N - Moves you to the north.")
		print("SOUTH or S - Moves you to the south.")
		print("EAST or E  - Moves you to the east.")
		print("WEST or W  - Moves you to the west.")
		print("QUIT       - Ends the adventure.")
		print("")

	elif x == "LOOK" or x == "L":

		Room(name).draw()

	elif x == "QUESTS":

		items = generate_items(sys.argv[2])
		rooms = create_rooms(read_paths(sys.argv[1]))

		quests = generate_quests(sys.argv[3], items, rooms)

		n = len(quests)

		for x in range(0, len(quests)):
			try:
				if x == 0:
					print("#0" + str(x) + ": " + str(quests[x][0]) + "   " + "- " + str(quests[x][2]))
				elif x > 0:
					print("#0" + str(int(x/2)) + ": " + str(quests[x][0]) + "   " + "- " + str(quests[x][2]))
				else:
					print("#" + str(x) + ": " + str(quests[x][0]) + "   " + "- " + str(quests[x][2]))
			except IndexError:
				pass
	
	elif x == "INV":
		print("You are carrying:")
		inventory = Adventurer().get_inv()
		if len(inventory) == 0:
			print("Nothing.")
		else:
			for x in range(0, len(inventory)):
				print("- A " + inventory[x])

	elif x == "CHECK":
		source = sys.argv[2]
		nom = input("Check what? ")

		items = generate_items(source)
		q = 0

		for x in range(0, len(items)):
			if nom == items[x][0] or nom.upper() == items[x][1]:
				Item(items[x][0], items[x][1], items[x][2], items[x][3])
				print("")
				Item(items[x][0], items[x][1], items[x][2], items[x][3]).get_info()
				print("")
				q = 1
			else:
				pass
		if q == 0:
			print("")
			print("You don't have that!")
			print("")
		else:
			pass

	elif x == "NORTH" or x == "N":
		for x in range(0, len(paths)):
			if paths[x][0] == current_room and "NORTH" == paths[x][1]:
				current_room = paths[x][2]
				Room(current_room).draw(north, south, east, west)
				break
			else:
				print("You can't go that way.")
				print("")
				break

	elif x == "SOUTH" or x == "S":
		for x in range(0, len(paths)):
			if paths[x][0] == current_room and "SOUTH" == paths[x][1]:
				current_room = paths[x][2]
				Room(current_room).draw(north, south, east, west)
				break
			else:
				print("You can't go that way.")
				print("")
				break

	elif x == "EAST" or x == "E":
		for x in range(0, len(paths)):
			if paths[x][0] == current_room and "EAST" == paths[x][1]:
				current_room = paths[x][2]
				Room(current_room).draw(north, south, east, west)
				break
			else:
				print("You can't go that way.")
				print("")
				break

	elif x == "WEST" or x == "W":
		for x in range(0, len(paths)):
			if paths[x][0] == current_room and "WEST" == paths[x][1]:
				current_room = paths[x][2]
				Room(current_room).draw(north, south, east, west)
				break
			else:
				print("You can't go that way.")
				print("")
				break



