class Adventurer:
    def __init__(self):
        """TODO: Initialises an adventurer object."""

        self.skill = 5
        self.will = 5
        self.inventory = []

    def get_inv(self):
        """TODO: Returns the adventurer's inventory."""

        return self.inventory


    def get_skill(self):
        """TODO: Returns the adventurer's skill level (before item bonuses are applied)."""

        return self.skill

    def get_will(self):
        """TODO: Returns the adventurer's will power (before item bonuses are applied).

        HINT: Can you make a more useful version of this method?"""

        return self.will

    def take(self, item):
        """TODO: Adds an item to the adventurer's inventory."""

        self.inventory.append(item)

    def check_self(self):
        """TODO: Shows adventurer stats and all item stats."""

        print("You are an adventurer, with a SKILL of {} and a WILL of {}.".format(get_skill(), get_will()))
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

		print(get_name())
		print("Grants a bonus of {} to SKILL.".format(get_skill()))
		print("Grants a bonus of {} to WILL".format(get_will()))

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
		self.completion = False

	def get_info(self):
		"""TODO: Returns the quest's description."""

		return self.desc

	def is_complete(self):
		"""TODO: Returns whether or not the quest is complete."""
		if self.completion == False:
			return False
		return True

	def get_action(self):
		"""TODO: Returns a command that the user can input to attempt the quest."""
		return self.action

	def get_room_desc(self):
		"""TODO: Returns a description for the room that the quest is currently in. Note that this is different depending on whether or not the quest has been completed."""
		print("You are standing at the {}".format(get_info()))
		if is_complete() == False:
			print(self.fail_msg)
		else:
			print(self.pass_msg)

	def attempt(self, player):
		"""TODO: Allows the player to attempt this quest.

		Check the cumulative skill or will power of the player and all their items. If this value is larger than the required skill or will threshold for this quest's completion, they succeed and are rewarded with an item (the room's description will also change because of this).

		Otherwise, nothing happens."""

		get_action()
		if player.skill >= self.req[2] or player.will >= self.req[2]:

			return self.pass_msg
		else:
			return self.fail_msg
class Room:
	def __init__(self, name):
		"""TODO: Initialises a room. Do not change the function signature (line 2)."""

		self.name = name
		self.north = None
		self.east = None
		self.west = None
		self.south = None

	def get_name(self):
		"""TODO: Returns the room's name."""

		return self.name

	def get_short_desc(self):
		"""TODO: Returns a string containing a short description of the room. This description changes based on whether or not a relevant quest has been completed in this room.

		If there are no quests that are relevant to this room, this should return: 'There is nothing in this room.' """
		if self.quest == None:
			return "There is nothing in this room."
		else:
			return self.quest.get_short_desc()

	def set_quest(self, quest):
		self.quest = quest

	def get_quest_action(self):
		"""TODO: If a quest can be completed in this room, returns a command that the user can input to attempt the quest."""
		if self.quest == None:
			pass
		else:
			return self.quest.get_quest_action()

	def get_quest(self):
		"""TODO: Returns a Quest object that can be completed in this room."""
		return self.quest

	def set_path(self, dir, dest):
		"""TODO: Creates an path leading from this room to another."""

		if dir == "NORTH":
			self.north = dest

		elif dir == "WEST":
			self.west = dest

		elif dir == "EAST":
			self.east = dest

		elif dir == "SOUTH":
			self.south = dest

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
		if dir == "NORTH":
			self.north.draw()
			return self.north
		elif dir == "EAST":
			self.east.draw()
			return self.east
		elif dir == "WEST":
			self.west.draw()
			return self.west
		elif dir == "SOUTH":
			self.south.draw()
			return self.south
		else:
			print("You can't go that way.")
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
	f = open(source, 'r')
	paths_x = f.readlines()
	if len(paths_x) == 0:
		print("No rooms exist! Exiting program...")
		sys.exit()
	else:
		pass
		while True:
			if paths_x == '':
				break
			else:
				path = paths_x.strip()
				path = path.split(">")
				paths.append(path)
	return paths
	f.close()
#reads from a file consisting of the paths and separate the origin, direction ..
# ..and destination which is appended into a paths list
def create_rooms(paths):
	"""Receives a list of paths and returns a list of rooms based on those paths. Each room will be generated in the order that they are found."""

	i=0
	rooms = []
	rooms1 = {}
	while i < len(paths):
		if paths[i][0].strip() not in rooms1:
			rooms1[paths[i][0]] = Room(paths[i][0])
		if paths[i][2].strip() not in rooms1:
			rooms1[paths[i][2]] = Room(paths[i][2])

		rooms1[paths[i][0]].set_path(paths[i][1], rooms1[paths[i][2]])
		i+=1

	stored = rooms1.values()
	for line in rooms1:
		rooms.append(rooms1[line])

	return rooms

def generate_items(source):
	"""Returns a list of items according to the specifications in a config file, (source).

	source contains item specifications of the form:
	item name | shortname | skill bonus | will bonus
	"""

	# TODO
	source = sys.argv[2]
	items = []
	f = open(source, 'r')
	items_x = f.readlines()
	while True:
		if items_x == '':
			break
		else:
			item = items_x.strip()
			item = item.split("|")
			items.append(item)

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
	f = open(source, 'r')
	quests_x = f.readline()
	while True:
		if quests_x == '':
			break
		else:
			quest = quests_x.strip()
			quest = quest.split("|")
			quests.append(quest)
	#while i < len(quests):
	#	quests[i][8]  #quest location

	return quests


# TODO: Retrieve info from CONFIG files. Use this information to make...
# ...Adventurer, Item, Quest, and Room objects.

if len(sys.argv) < 4:
	print("Usage: python3 simulation.py <paths> <items> <quests>")
	sys.exit()
#When fewer than 3 command-line arguments are being supplied, this will...
#...cause the program to exit instead
try:
	open_paths = open(sys.argv[1], 'r')
	open_items = open(sys.argv[2], 'r')
	open_quests = open(sys.argv[3], 'r')

	open_paths.close()
	open_items.close()
	open_quests.close()

except FileNotFoundError:
	print("Please specify a valid configuration file.")
	sys.exit()
#When there is an invalid file that is being given, the program will exit

# TODO: Receive commands from standard input and act appropriately.

TeAroha = Adventurer() #initiating the Adventurer

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
	x = input(">>> ")

	if x == "QUIT":
		print("Bye!")
		exit()

	elif x == "HELP":
		print("HELP       - Shows some available commands.")
		print("LOOK OR L  - Lets you see the map/room again.")
		print("QUESTS     - Lists all your active and completed quests.")
		print("INV        - Lists all the items in your inventory.")
		print("CHECK      - Lets you see an item (or yourself) in more details.")
		print("NORTH OR N - Moves you to the north.")
		print("SOUTH OR S - Moves you to the south.")
		print("EAST OR E  - Moves you to the east.")
		print("WEST OR W  - Moves you to the west.")
		print("QUIT       - Ends the adventure.")

	elif x == "QUESTS": #import name and action from quests.py
		generate_quests(source, items, rooms)

		items = generate_items(sys.argv[2])
		rooms = create_rooms(read_paths(sys.argv[1]))

		quests = generate_quests(sys.argv[3], items, rooms)

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

	elif x == "INV":
		inventory = TeAroha.get_inv()
		print("You are carrying:")
		if len(inventory) == 0:
			print("Nothing.")
		else:
			i=0
			while i < len(inventory):
				print("- A {}".format(inventory[i]))
				i+=1

	elif x == "CHECK":
		source = sys.argv[2]
		nom = input("Check what? ")

		
		if w == "ME":
			print(Adventurer().check_self())
			
		items = generate_items(source)
		i=0

		for x in range(0, len(items)):
			if y == items[x][0] or y.upper() == items[x][1]:
				Item(items[x][0], items[x][1], items[x][2], items[x][3])
				print("")
				Item(items[x][0], items[x][1], items[x][2], items[x][3]).get_info()
				print("")
				i = 1
			else:
				pass
		if i == 0:
			print("")
			print("You don't have that!")
			print("")
			
	elif x == "LOOK" or x == "L":
		Room(name).draw()
	else:
		print("You can't do that.\n")

