import serial
import time
import pyautogui


counterSpace = 0

pwdPres = False




def send_command_check(ser, command, delay =1, max_waiting_time = 600):
    ser.write((command + '\r\n').encode('ascii'))
    time.sleep(delay)
    start_time = time.time()
    output = ""
    global counterSpace
    global pwdPres
    pwdPres = False
    while time.time() - start_time < max_waiting_time:
        time.sleep(delay)
        new_data = ser.read(ser.in_waiting).decode('ascii')
        output += new_data
        if "Password:" in new_data:
            print("Device is password protected")
            pwdPres = True
            break
        if len(new_data) >= 1:
            counterSpace = 1
            
            print("Device is configured and called ")
            break
        if "" in new_data and counterSpace == 0:
            empCommand = True
            counterSpace =1
            break

    return output

def send_command_Erase(ser, command, delay =1, max_waiting_time = 600):
    ser.write((command + '\r\n').encode('ascii'))
    time.sleep(delay)
    start_time = time.time()
    output = ""
    global counterSpace
    while time.time() - start_time < max_waiting_time:
        time.sleep(delay)
        new_data = ser.read(ser.in_waiting).decode('ascii')
        output += new_data
        
        if len(new_data) >= 1:
            counterSpace = 1
            break
        if "" in new_data and counterSpace == 0:
            empCommand = True
            counterSpace =1
            break

    return output

def send_command(ser, command, hostname, delay =1, max_waiting_time = 600,):
    ser.write((command + '\r\n').encode('ascii'))
    time.sleep(delay)
    start_time = time.time()
    output = ""
    global counterSpace

    counter =0
    while time.time() - start_time < max_waiting_time:
        time.sleep(delay)
        new_data = ser.read(ser.in_waiting).decode('ascii')
        output += new_data
        
        if counter == 25:
            break
            
        if "Press RETURN to get started!" in new_data:
            counterSpace = 1
            break
            
        if "Would you like to enter the initial configuration dialog? [yes/no]:" in new_data:
            counterSpace =1
            break
        # Check if the router has finished printing
        #R1(config)#
        if (hostname+">" in new_data or
            hostname+"(config)#" in new_data or
            hostname+"#" in new_data or
            hostname+"int#" in new_data or 
            "Router#" in new_data or
            "Switch#" in new_data or 
            "Router>" in new_data or 
            "Switch>" in new_data): 
            
            counterSpace =1
            break
        if "" in new_data and counterSpace == 0:
            empCommand = True

            counterSpace =1
            break
        counter += 1

    return output

def read_commands_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            
            allText = [line.strip() for line in file.readlines()]

            hostname = allText[0]
            commands = allText[1:]
        return commands, hostname
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []


def main():
    empCommand: bool = False
    ext: bool = True
    print("******************************************")
    print("Welcome to Cisco Device Commander")
    print("This program will run commands and/or ")
    print("output the results to a txt file.")
    print("******************************************")

    # Configure your serial port parameters
    print("")
    print("Enter your console cable number EX: COM3")
    print("This can be found in device manager")
    userCom: int = input("Enter COM number: ")
    serial_port = "COM"+userCom  # Change this to a serial port (e.g., 'COM1' on Windows)
    baud_rate = 9600

    global counterSpace
    counterSpace = 0
    

    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    
    while ext == True:
    
        print("")
        print("******************************************")
        print("List of what to choice")
        print("1: [E]rase and reload the device")
        print("2: [M]Runs Default commands")
        print("3: [S]ee if router is password pretected")
        print("      or if the router is in use")
        print("4: [Z]Wakes up device with three spaces ")
        print("5: [C]looks for a command.txt and runs")
        print("      said set of commands in order T->B")
        print("      Format:")
        print("      'en'")
        print("      'show running-config'")
        print("      'show ip conf bri'")
        print("5: [D]one - leave program")
        print("")
        print("******************************************")
        userChoice = input("Input E or C etc.: ")
        
        #**************************************************
        if (userChoice == "D" or userChoice == "d"):
            ext = False

        if (userChoice == "c" or userChoice == "C"): 
            print("To break and go back to the Menu <ctl> + c ")
            print("Looking for commands.txt")  
            commands, hostname = read_commands_from_file('commands.txt')

            print(f"Hostname of Router {hostname}")
            if not commands:
                print("No commands found in the file. Exiting.")
                return
            
            output_file = input("Enter the output file.txt name, EX<Something>): ")+'.txt'

            try:
                while True:
                    with open(output_file, 'w') as f:
                        for command in commands:
                            # Send command and get output
                            output = send_command(ser, command, hostname)
                            if empCommand:
                                output = send_command(ser, '')
                                empCommand = False
                            f.write(f"\n\n### {command} ###\n\n")
                            print(command)
                            f.write(output)
                            print(output)

                    user_exit = input("Are you done? Enter [E]xit or [C]ontinue")
                    if user_exit == "E" or user_exit == "e":
                        break  # Break out of the loop on user input

            except KeyboardInterrupt:
                print("Ctrl+C was pressed. Exiting the program.")





        #**************************************************
        elif (userChoice == "z" or userChoice == "Z"): 
            commands = [
                '',
                '',
                ''
            ]
            
            for command in commands:
                # Send command and get output
                output = send_command_Erase(ser, command)
                if empCommand == True:
                    output = send_command_Erase(ser, '')
                    empCommand = False
                
                print (command)
                
                print (output)
            print("******************************************")
            print("Device woken up")
            userExit = input("Are you done? Enter [E]xit or [C]ontinue")
            if userExit == "E" or userExit == "e":
                ext = False
            else:
                ext = True


        #**************************************************
        if (userChoice == "M" or userChoice == "m"):
            print("To break and go back to the Menu <ctl> + c ")
            print("If hostname is default router or switch leave blank")
            hostname = input("Input Device hostname: ")
            output_file = input("Enter the output file name, Something.txt): ")+'.txt'  # Prompt user for output file name    
            # Commands to run on the Cisco device
            commands = [
                '',
                'no',
                #' ',
                '',
                'en',
                'terminal length 0',
                'show version',
                'show inventory',
                'show interfaces',
                'show ipv6 interface brief',
                'show sdm prefer',
                # 'configure terminal',
                # 'sdm prefer dual-ipv4-and-ipv6 routing',
                '',

                

                # Add more commands as needed
            ]
            
            # Create and open a file to write the output
            #output_file = 'cisco_output.txt'
            try:
                with open(output_file, 'w') as f:
                    for command in commands:
                        # Send command and get output
                        output = send_command(ser, command, hostname)
                        if empCommand == True:
                            output = send_command(ser, '')
                            empCommand = False
                        f.write(f"\n\n### {command} ###\n\n")
                        print (command)
                        f.write(output)
                        print (output)
                userExit = input("Are you done? Enter [E]xit or [C]ontinue")
                if userExit == "E" or userExit == "e":
                    ext = False
                else:
                    ext = True
            except KeyboardInterrupt:
                print("Ctrl+C was pressed. Exiting the program.")


        #**************************************************
        elif (userChoice == "E" or userChoice == "e"): 
            commands = [
                '',
                'en',
                'erase startup-config',
                '',
                'reload',
                '',
                'no',
                '',

                # Add more commands as needed
            ]
            
            # Create and open a file to write the output
            #output_file = 'cisco_output.txt'
            
            
            for command in commands:
                # Send command and get output
                output = send_command_Erase(ser, command)
                if empCommand == True:
                    output = send_command_Erase(ser, '')
                    empCommand = False
                
                print (command)
                
                print (output)
            print("******************************************")
            print("Reload is done may take several minutes")
            userExit = input("Are you done? Enter [E]xit or [C]ontinue")
            if userExit == "E" or userExit == "e":
                ext = False
            else:
                ext = True



        #**************************************************
        elif (userChoice == "S" or userChoice == "s"): 
            commands = [
                '',
                'en',
                'configure terminal',
                ''

                # Add more commands as needed
            ]
            
            # Create and open a file to write the output
            #output_file = 'cisco_output.txt'
            global pwdPres
            
            pwdPres = False
            
            
            for command in commands:
                # Send command and get output
                output = send_command_check(ser, command)
                if empCommand == True:
                    output = send_command_check(ser, '')
                    empCommand = False
                
                print (output)
                if pwdPres == True:
                    break
                #print (command)
                
                
            if pwdPres == False:
                print("No passwords are detected")
            print()
            userExit = input("Are you done? Enter [E]xit or [C]ontinue")
            if userExit == "E" or userExit == "e":
                ext = False
            else:
                ext = True
                
    # Close the serial port
    ser.close()

if __name__ == "__main__":
    main()
