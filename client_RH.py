import socket 
import sys

def user_input():
    try:
        command  = input("> ").split()
        return command
    except EOFError:
        sys.exit() # DONE

def send_server(command):
    length = (str(len(command))).ljust(256, " ").encode('ascii')
    message = command.encode('ascii')
    s.send(length)
    s.send(message) # DONE

def receive_server():
    length = int(s.recv(256).decode('ascii', 'ignore').strip("\x00"))
    received = s.recv(length).decode('ascii', 'ignore')
    if received.split(" ")[0] == "ok":
        success = True
    else:
        success = False
    return received, success # DONE

def server_comm(command):
    send_server(command)
    received = receive_server()
    return received # DONE

def invocation_message(): # DONE
    print("cannot invoke the command in this state")

def check_valid(command):
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
    return returned# DONE # DONE

def terrain_processing(data_point, rover_elevation, is_rover):
    current_elevation = ""
    i = 5 
    while True:
        if data_point[i] != ",":
            current_elevation += data_point[i]
            i += 1
        else:
            break
    relative_elevation = int(current_elevation) - rover_elevation
    rover = int(data_point[i+1])
    message = int(data_point[i+3])

    if (rover == 1 and message == 1) or (rover == 1 and message == 0): 
        print("R", end = "")
    elif rover == 0 and message == 1:
        print("M", end = "")
    else:
        print(" ", end = "")

    if is_rover: 
        print("R", end = "")
    else:
        if relative_elevation > 9:
            print("9", end = "")
        elif relative_elevation < 0: 
            print("-", end = "")
        elif relative_elevation == 0:
            print(" ", end = "")
        else: print("{}".format(relative_elevation), end = "")

    print("|", end = "") # DONE

connected = False
verified = False
terrain_data = []

while True:
    command = user_input()
    if len(command) == 0: 
        continue

    elif command[0] == "quit": 
        if connected == True:
            message = server_comm("quit")
            if message[1] == True:
                s.close()
                sys.exit()
        else: 
            sys.exit()

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

    elif (command[0] == "login" and check_valid("login")):
        if len(command) < 3:
            print("Incomplete login criteria")
        else:
            ident = command[1]
            password = command[2]
            message = " ".join([command[0], ident, password])
            received = server_comm(message)
            if received[1] == True:
                print("Logged In!")
                verified = True
            elif received[1] == False:
                print("Invalid login details")

    elif command[0] == "observe" and check_valid("observe"):
        received_data = server_comm("action observe")[0].strip("ok observe ").split() 
        print()

        rover_elevation_string = ""
        i = 5 
        while True:
            if received_data[17][i] != ",":
                rover_elevation_string += received_data[17][i]
                i += 1
            else:
                break
        rover_elevation = int(rover_elevation_string) 

        for i in range (0, len(received_data)):
            if i%7 == 0:
                print("|", end = "") 
            if i == 17:
                is_rover = True
            else: 
                is_rover = False
            terrain_processing(received_data[i], rover_elevation, is_rover) 

            if (i+1)%7 == 0:
                print() 
        
        for i in range(0, len(received_data)):
            new_terrain = (int(received_data[i][1]),int(received_data[i][3]))
            terrain_data.append(new_terrain)
    
    elif ((command[0] == "move" and check_valid("move")) or (command[0] == "m" and check_valid("m"))) and len(command) >= 2 :
        message = "action move "
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
        received = server_comm(message)
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))
    
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
    
    elif command[0] == "inspect" and check_valid("inspect") and len(command) >= 2:
        message = "action inspect "
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

        received = server_comm(message)
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))
        else:
            if received[0].strip("ok inspect") == "":
                print("Nothing interesting was found here")
            else:
                message = received[0].strip("ok inspect ").strip("(").strip(")")
                print("You found a note: {}".format(message))
    
    elif command[0] == "note" and check_valid("note") and len(command) >= 2:
        message = "action note "
        for i in range(1, len(command)-1):
            message += command[i] 
            message += " "
        message += command[len(command)-1]

        received = server_comm(message)
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))

    elif command[0] == "message" and check_valid("message") and len(command) >= 3:
        message = "action message "
        for i in range(1, len(command)-1):
            message += command[i] 
            message += " "
        message += command[len(command)-1]

        received = server_comm(message)
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))

    elif command[0] == "commit" and check_valid("commit"):
        message = "action commit "
        for i in range(0, len(terrain_data)):
            single_data = str(terrain_data[i])
            formatted_data = "(" + single_data[1] + "," + single_data[4] + ")"
            message += formatted_data
            if i != len(terrain_data)-1:
                message += " "
        received = server_comm(message)
        if received[1] == False:
            print("Error: {}".format(received[0].strip("error ")))                

    else: 
        print("invalid command")
    

    
