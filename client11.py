import socket 
import sys
from multiprocessing import Process

def user_input(): # user input formatted
    try:
        command  = input("> ").split()
        return command
    except EOFError:
        sys.exit()

def send_server(command): # deals with messages sent to the server
    length = (str(len(command))).ljust(256, " ").encode('ascii')
    message = command.encode('ascii')
    s.send(length)
    s.send(message)

def receive_server(): # deals with messages received from the server 
    length = int(s.recv(256).decode('ascii', 'ignore').strip("\x00"))
    received = s.recv(length).decode('ascii', 'ignore')
    if received.split(" ")[0] == "ok": # if command has been successfully completed, success is true, else an error message is needed
        success = True
    else:
        success = False
    return received, success

def server_comm(command): # sending and receiving in one method
    send_server(command)
    received = receive_server()
    return received

def invocation_message():
    print("cannot invoke the command in this state")

def check_valid(command): # checking if command is permitted in the current state
    returned = True
    if ((connected == False) and (command != "connect")):
        invocation_message()
        returned = False
    elif ((connected == True) and (verified == False) and (command != "login")):
        invocation_message()
        returned = False
    elif ((connected == True) and (verified == True) and ((command == "connect") or (command == "login"))):
        invocation_message()
        returned = False
    return returned

def find_elevation(data_point): # finding the elevation of a tuple
    comma_counter = 0
    start = 0
    while start < len(data_point):
        if data_point[start] == ",":
            comma_counter += 1
            if comma_counter == 2:
                start += 1
                break
        start += 1
    return start

### OBSERVE ###
''' Each observe block is made up of 35 LR| blocks. This method handles the printing of those 3.'''
def terrain_processing(data_point, rover_elevation, is_rover): 

    start = find_elevation(data_point)

    current_elevation = "" # x and y not needed here, so starting index bypasses the initial x and y
    i = start
    while True:
        if data_point[i] != ",":
            current_elevation += data_point[i]
            i += 1
        else:
            break
    relative_elevation = int(current_elevation) - rover_elevation
    rover = int(data_point[i+1])
    message = int(data_point[i+3])

    if (rover == 1 and message == 1) or (rover == 1 and message == 0): # printing L
        print("R", end = "")
    elif rover == 0 and message == 1:
        print("M", end = "")
    else:
        print(" ", end = "")

    if is_rover:  # if it is the rover, print R instead of relative elevation
        print("R", end = "")
    else: # printing R
        if relative_elevation > 9:
            print("9", end = "")
        elif relative_elevation < 0: 
            print("-", end = "")
        elif relative_elevation == 0:
            print(" ", end = "")
        else: print("{}".format(relative_elevation), end = "")

    print("|", end = "")  # printing |

def server_messages(s): # function used in multiprocessing
    received_message = receive_server() 
    server_message = received_message[0]

    message_split = server_message.split()
    if message_split[0] == "event": 
        ### MESSAGE ###
        if message_split[1] == "message":
            message = ""
            for i in range (3, len(message_split)):
                message += message_split[i]
                if i != len(message_split) - 1:
                    message += " "
            print("{}: {}".format(message_split[2], message))
        ### NOTIFY ###
        elif message_split[1] == "notify": 
            message = ""
            for i in range (2, len(message_split)):
                message += message_split[i]
                if i != len(message_split) - 1:
                    message += " "
            print("Server: {}".format(message))
        print("> ", end = "")
    elif message_split[0] == "error":
        print("Error: {}".format(message_split[0].strip("error ")))
    
def check_for_error(received): # if error message is thrown, format and print
    if received[1] == False:
        print("Error: {}".format(received[0].strip("error ")))
        return False
    return True

def format_command(command, message): # format command for note and message
    for i in range(1, len(command)):
        message += command[i] 
        if i != len(command) -1 :
            message += " "
    return message

def receive_and_check(message): # receive from server and then check for an error 
    received = server_comm(message)
    check_for_error(received)

def message_direction(command, message): # formatting message where directions are involved
    if command[1] == "north" or command[1] == "n":
        message += "north"
    elif command[1] == "south" or command[1] == "s":
        message += "south"
    elif command[1] == "east" or command[1] == "e":
        message += "east"
    elif command[1] == "west" or command[1] == "w":
        message += "west"
    else:
        print("invalid command")
    return message

    
connected = False
verified = False
terrain_data = []
process_create = False # once logged in, program should create subprocess that checks for server message

while True:
    if process_create == True: # checks for server message, before terminating process in order to prevent server interference later on
        p = Process(target = server_messages, args = (s, ))
        p.daemon = True # if main process ends, all other subprocesses end with it
        p.start()
        command = user_input()
        p.terminate()
    if process_create == False:
        command = user_input()

    if len(command) == 0: # handling ENTER as keyboard input 
        print("invalid command")

    # not enough inputs
    elif (((command[0] == "move" and len(command) < 2) or (command[0] == "inspect" and len(command) < 2) or (command[0] == "note" and len(command) < 2) or (command[0] == "message" and len(command) < 3))):
        if check_valid(command[0]) == True: # when there are not enough inputs, but it is in the right state
            print("invalid command")
    
    ### QUIT ###
    elif command[0] == "quit": 
        if connected == True:
            message = server_comm("quit")
            if message[1] == True:
                s.close()
                sys.exit()
        else: 
            sys.exit()

    ### CONNECT ###
    elif command[0] == "connect" and check_valid("connect"):
        try: 
            hostname = command[1]
            port = int(command[2])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((hostname, port))
            message = receive_server()
            if message[1] == True:
                print("Connected, please log in")
                connected = True
            elif message[1] == False:
                print("Error: {}".format(message[0].strip("error ")))
        except Exception:
            print("Unable to connect to the server, check command arguments")

    ### LOGIN ###
    elif (command[0] == "login" and check_valid("login")):
        if len(command) < 3: # either ident or password not given
            print("Incomplete login criteria")
        else:
            ident = command[1]
            password = command[2]
            message = " ".join([command[0], ident, password])
            received = server_comm(message)
            if received[1] == True:
                print("Logged In!")
                verified = True
                process_create = True
            elif received[1] == False:
                print("Invalid login details")

    ### OBSERVE ###
    elif command[0] == "observe" and check_valid("observe"):
        received_data = server_comm("action observe")[0].strip("ok observe ").split() 
        print()

        # finding rover elevation for later use in relative heights
        start = find_elevation(received_data[17])

        rover_elevation_string = ""
        i = start
        while True:
            if received_data[17][i] != ",":
                rover_elevation_string += received_data[17][i]
                i += 1
            else:
                break
        rover_elevation = int(rover_elevation_string) 

        # printing out grid 
        for i in range (0, len(received_data)):
            if i%7 == 0:
                print("|", end = "") # prints first | in each row
            if i == 17:
                is_rover = True
            else: 
                is_rover = False
            terrain_processing(received_data[i], rover_elevation, is_rover) 

            if (i+1)%7 == 0: # prints new line every 7 tuples
                print() 
        
        for i in range(0, len(received_data)): # saves observed data for later committing
            x = ""
            y = ""
            comma_counter = 0
            g = 1
            while g < len(received_data[i]): # finds x and y values when they are greater than one digit
                if received_data[i][g] == ",":
                    comma_counter += 1
                    if comma_counter == 2: # If g passes x and y, the later information is no longer needed for commit
                        break
                elif comma_counter == 0:
                    x += received_data[i][g]
                elif comma_counter == 1:
                    y += received_data[i][g]
                g += 1

            new_terrain = (int(x),int(y))
            terrain_data.append(new_terrain)
    
    ### MOVE ###
    elif ((command[0] == "move" and check_valid("move")) or (command[0] == "m" and check_valid("m"))) and len(command) >= 2 :
        message = "action move "
        message = message_direction(command, message)
        receive_and_check(message)
    
    ### STATS ###
    elif command[0] == "stats" and check_valid("stats"):
        received = server_comm("action stats")
        
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))
        else:
            stats = received[0].strip("ok stats (").strip(")").split(",")
            x = int(stats[0])
            y = int(stats[1])
            explored = int(stats[2])

            print("Number of tiles explored: {}".format(explored))
            print("Current position: ({},{})".format(x,y))
    
    ### INSPECT ###
    elif command[0] == "inspect"  and len(command) >= 2 and check_valid("inspect"): 
        message = "action inspect "
        message = message_direction(command, message)

        received = server_comm(message)
        if check_for_error(received):
            if received[0].strip("ok inspect") == "":
                print("Nothing interesting was found here")
            else:
                new_message = received[0].strip("ok inspect ").strip("(").strip(")")
                print("You found a note: {}".format(new_message))
    
    ### NOTE ###
    elif command[0] == "note" and check_valid("note") and len(command) >= 2:
        message = "action note "
        new_message = format_command(command, message)
        receive_and_check(new_message)

    ### MESSAGE ###
    elif command[0] == "message" and check_valid("message") and len(command) >= 3:
        message = "action message "
        new_message = format_command(command, message)
        receive_and_check(new_message)

    ### COMMIT ###
    elif command[0] == "commit" and check_valid("commit"):
        message = "action commit "
        for i in range(0, len(terrain_data)):
            single_data = terrain_data[i]
            formatted_data = "(" + str(single_data[0]) + "," + str(single_data[1]) + ")"
            message += formatted_data
            if i != len(terrain_data)-1:
                message += " "
        receive_and_check(message)     

    # random input
    elif command[0] != "connect" and command[0] != "login" and command[0] != "observe" and command[0] != "move" and command[0] != "stats" and command[0] != "inspect" and command[0] != "note" and command[0] != "message" and command[0] != "quit": 
        print("invalid command")
    
