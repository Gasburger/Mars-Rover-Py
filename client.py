import socket
import sys
#from server_defs import server, send, receive
#from message_handling import invoke, grid_map, is_valid

#Write your code here and in other files you create!
def server(cmd):
	send(cmd)
	rcv = receive()
	return rcv

def send(cmd):
	
	l = (str(len(cmd))).ljust(256, " ").encode("ascii")
	msg = cmd.encode("ascii")
	s.send(l)
	s.send(msg)

def receive():
	l = int(s.recv(256).decode('ascii', 'ignore').strip("\x00"))
	rcvd = s.recv(l).decode('ascii', 'ignore')

	if rcvd.split(" ")[0] == "ok":
		gg = True

	else:
		gg = False

	return gg, rcvd

is_con = False
verify = False
grid = []

def invoke():
	print("cannot invoke the command in this state")

def find(point): # finding the elevation of a tuple
	c = 0
	st = 0
	while st < len(point):
		if point[st] == ",":
			c += 1
			if c == 2:
				st += 1
				break
		st += 1
	return st

def grid_map(point, height, rover_status):

	st = find(point)
	altitude = ""

	while True:
		if point[st] != ",":
			altitude += point[st]
			st += 1
		else:
			break

	rel_alt = int(altitude) - height
	m = int(point[st+3])
	r = int(point[st+1])

	if (r == 1 and m == 1) or (r == 1 and m == 0):
		print("R", end = "")

	elif int(point[st+1]) == 0 and int(point[st+3]) == 1:
		print("M", end = "")

	else:
		print(" ", end = "")

	if rover_status:
		print("R", end = "")

	else:
		if rel_alt == 0:
			print(" ", end = "")

		elif rel_alt < 0:
			print("-", end = "")

		elif rel_alt > 9:
			print("9", end = "")

		else:
			print(rel_alt, end = "")

	print("|", end = "")

def is_valid(cmd):
	b = True

	if cmd != "connect" and not is_con:
		invoke()
		b = False

	elif is_con and verify and (cmd == "connect" or cmd == "login"):
		invoke()
		b = False

	elif (is_con and not verify) and cmd != "login":
		invoke()
		b = False

	return b

while True:
	try:
		cmd = input("> ").split()
	except EOFError:
		exit()


	if len(cmd) == 0:
		#pass
		continue

	elif cmd[0] == "connect" and is_valid("connect"):
		host = cmd[1]
		port = int(cmd[2])

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host, port))
			msg = receive()

			if msg[0]:
				print("Connected, please log in")
				is_con = True

			else:
				print("Error: " + str(rcvd[1].strip("error ")))	

		except:
			print("Unable to connect to the server, check command arguments")

	elif cmd[0] == "login" and is_valid("login"):

		if len(cmd) != 3:
			print("Incomplete login criteria")

		else:
			msg = " ".join([cmd[0], cmd[1], cmd[2]])
			rcvd = server(msg)

			if rcvd[0]:
				print("Logged In!")

				verify = True

			elif not rcvd[0]:
				print("Invalid login details")


	elif ((cmd[0] == "move" and is_valid("move")) or (cmd[0] == "m" and is_valid("m"))) and len(cmd) >= 2 :
		msg = "action move "

		if cmd[1] == "north" or cmd[1] == "n":
			msg += "north"

		elif cmd[1] == "south" or cmd[1] == "s":
			msg += "south"

		elif cmd[1] == "east" or cmd[1] == "e":
			msg += "east"

		elif cmd[1] == "west" or cmd[1] == "w":
			msg += "west"

		else:
			print("invalid command")

		rcvd = server(msg)
		if rcvd[0] == False:
			print("Error: {}".format(rcvd[1].strip("error ")))


	elif cmd[0] == "stats" and is_valid("stats"):
		rcvd = server("action stats")

		if rcvd[0]:
			info_l = rcvd[1].strip("ok stats (").strip(")").split(",")
			print("Number of tiles explored: {}".format(info_l[2]))
			print("Current position: ({},{})".format(info_l[0],info_l[1]))


		else:
			print("Error: " + str(rcvd[1].strip("error ")))


	elif cmd[0] == "observe" and is_valid("observe"):
		intercepted = server("action observe")[1].strip("ok observe ").split()
		print()

		st = find(intercepted[17])

		height_str = ""

		while True:
			if intercepted[17][st] != ",":
				height_str += intercepted[17][st]
				st += 1
			else:
				break
		height_n = int(height_str)

		for y in range(0, len(intercepted)):
			if y % 7 == 0:
				print("|", end = "")
			else:
				pass

			if y == 17:
				rover_status = True

			else:
				rover_status = False

			grid_map(intercepted[y], height_n, rover_status)

			if (y + 1) % 7 == 0:
				print()

		for x in range(0, len(intercepted)):
			c = 0
			t = 1
			i1 = ""
			i2 = ""
			
			while t < len(intercepted[x]): 
				if intercepted[x][t] == ",":
					c += 1
					if c == 2: 
						break
				elif c == 0:
					i1 += intercepted[x][t]
				elif c == 1:
					i2 += intercepted[x][t]
				t += 1

			new = (int(i1), int(i2))
			grid.append(new)

	elif cmd[0] == "note" and is_valid("note"):
		if len(cmd) > 1:
			msg = "action note "
			c = 1
			while c < len(cmd):
				if c != len(cmd) - 1:
					msg = msg + cmd[c] + " "
				else:
					msg = msg + cmd[c]
				c += 1

		rcvd = server(msg)
		if not rcvd[0]:
			print("Error: " + str(rcvd[1].strip("error ")))

		else:
			pass

	elif cmd[0] == "message" and is_valid("message"):
		if len(cmd) > 2:
			msg = "action message "
			c = 1
			while c < len(cmd):
				if c != len(cmd) - 1:
					msg = msg + cmd[c] + " "
				else:
					msg = msg + cmd[c]
				c += 1
		rcvd = server(msg)
		if not rcvd[0]:
			print("Error: " + str(rcvd[1].strip("error ")))

		else:
			pass

	elif cmd[0] == "commit" and is_valid("commit"):
		msg = "action commit "
		c = 0
		while c <= len(grid):
			unit = str(grid[c])
			full = "({},{})".format(unit[0], unit[1])

			if c != len(grid) - 1:
				msg = msg + full + " "
			else:
				msg += full

		rcvd = server(msg)
		if not rcvd[0]:
			print("Error: " + str(rcvd[1].strip("error ")))

		else:
			pass
	
	elif cmd[0] == "inspect" and is_valid("inspect"):
		if len(cmd) > 1:
			msg  = "action inspect "
			if cmd[1] == "north" or cmd[1] == "n":
				msg += "north"

			elif cmd[1] == "south" or cmd[1] == "s":
				msg += "south"

			elif cmd[1] == "west" or cmd[1] == "w":
				msg += "west"

			elif cmd[1] == "east" or cmd[1] == "e":
				msg += "east"

			else:
				print("invalid command")

		rcvd = server(msg)
		if not rcvd[0]:
			print("Error: " + str(rcvd[1].strip("error ")))

		else:
			if rcvd[1].strip("ok inspect") == "":
				print("Nothing interesting was found here")

			else:
				msg = rcvd[1].strip("ok inspect ").strip("(").strip(")")
				print("You found a note: " + str(msg))

	elif cmd[0] == "quit" :
		if is_con:
			msg = server("quit")
			if msg[0]:
				s.close()
				exit()
		else:
			exit()

	else:
		print("invalid command")