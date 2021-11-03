import sys
import socket
#import client

is_con = False
verify = False

def invoke():
	print("cannot invoke the command in this state")

def grid_map(point, height, rover_status):
	altitude = 0
	comma_index = 5

	while True:
		if point[comma_index] != ",":
			altitude += point[comma_index]
			comma_index += 1
		else:
			break

	rel_alt = altitude - height

	if int(data_point[i+1]) == 1 and int(data_point[i+3]) == 1 or int(data_point[i+3]) == 0:
		print("R ")

	elif int(data_point[i+1]) == 0 and int(data_point[i+3]) == 1:
		print("M ")

	else:
		print("  ")

	if rover_status:
		print("R ")
	else:
		if rel_alt == 0:
			print("  ")

		elif rel_alt < 0:
			print("- ")

		elif rel_alt > 9:
			print("9 ")

		else:
			print(rel_alt, "")

	print("| ")

def is_valid(cmd):
	b = True

	if cmd != "connect" and not is_con:
		invoke()
		b = False

	elif is_con and verify and cmd == "connect" or cmd == "login":
		invoke()
		b = False

	elif is_con and not verify and cmd != "login":
		invoke()
		b = False

	return b