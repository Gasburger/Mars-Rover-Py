quit
connect		connect y
login		login y
observe		move y
move		stats y
stats		observe y
inspect		note y
note		message y
message		commit y
commit		inspect y 
			quit y



	'''elif (cmd[0] == "m" and is_valid("m")) or (cmd[0] == "move" and is_valid("move")):
		if len(cmd) >= 2:
			msg = "action move"

			if cmd[1] == "n" or cmd[1] == "north":
				msg += "north"

			elif cmd[1] == "s" or cmd[1] == "south":
				msg += "south"

			elif cmd[1] == "w" or cmd[1] == "west":
				msg += "west"

			elif cmd[1] == "e" or cmd[1] == "east":
				msg += "east"

			else:
				print("Invalid command")

			rcvd = server(msg)

			if not rcvd[0]:
				print("Error: " + str(rcvd[1].strip("error ")))
		else:
			print("Invalid command")'''