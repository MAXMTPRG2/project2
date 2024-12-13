# Max Molnar 100746162
# TPRG 2131 CRN 02 -Project 2
# Dec 11th, 2024

# ClientMM.py

# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

# Program adapted from code/techniques provided by Professor Phil J

# The sources I used:
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_LED_Indicators_Text_Based.py
# https://www.pythontutorial.net/python-concurrency/python-threading-event/
# https://codingidol.com/how-to-get-output-from-subprocess-python/
# https://www.nicm.dev/vcgencmd/

# Connect to the server and collate and send 50 iterations of VCGENCMD command data
# in JSON format, Update the GUI/LED every 2 seconds to illustrate connection,
# client will not run on windows, only on raspberry Pi

import subprocess
import time
import socket
import PySimpleGUI as sg
import json
from pathlib import Path


IS_RPI = Path("/etc/rpi-issue").exists() #Used to check - Were using the pi
#If not using the Pi, gracefully exit
if (IS_RPI):
    print("Correct Hardware")
else:
    print("Not on a Raspberry Pi, Exiting...") #Exit if not using the Pi
    exit()


# Setup socket object and parameters
s = socket.socket()
host = '10.0.0.225' # Local host of the Pi, or loopback address
port = 8000

def collate_data(iteration):
    '''Function to get/collate vcgencmd command data'''
    # Use subprocess to avoid interupting the GUI, remove characters from VCGENCMD command values
    # and convert to float
    temp = float(subprocess.getoutput("vcgencmd measure_temp").split("=")[1].replace("'C", ""))
    voltage = float(subprocess.getoutput("vcgencmd measure_volts core").split("=")[1].replace("V", ""))
    clock = float(subprocess.getoutput("vcgencmd measure_clock core").split("=")[1])
    voltsram = float(subprocess.getoutput("vcgencmd measure_volts sdram_p").split("=")[1].replace("V", ""))
    memory = float(subprocess.getoutput("vcgencmd get_mem gpu").split("=")[1].replace("M", ""))
    # Formulate data into a dictionary and round to 1 decimal place
    data_dict = {"Core Temperature": round(temp,1), "Core Voltage": round(voltage,1), "Core Freq": round(clock,1),
                 "RAM Voltage": round(voltsram,1), "GPU Mem": round(memory,1), "Iteration": iteration}
    #Convert to JSON format
    json_dict = json.dumps(data_dict)
    return json_dict #Return JSON Data

def send_to_server(jsonmessage):
    '''Function to send json data to the server'''
    jsonbyte = bytearray(jsonmessage, "UTF-8") #Convert data to BYTES using UTF-8
    s.send(jsonbyte) # Send the data
    print("Data sent!")
    
    
def vcgencmd_gui():
    '''Main Function to handle GUI and Iterations 0 - 50'''
    # Add colour to the GUI 
    sg.theme('Light Blue')
    
    CIRCLE = '\u2B24'              #  Solid/LED ON
    CIRCLE_OUTLINE = '\u25EF'      #  Blank/LED OFF
    
    #Format the layout
    layout = [[sg.Text('Connection Indicator LED')],
            [sg.Push(), sg.Text(CIRCLE_OUTLINE, text_color='Red', key='-LED0-'), sg.Push()],
            [sg.Button('Exit')]]
    
    #Create the window
    window = sg.Window('Client Window - Max Molnar', layout, font='Any 16')
    try:
        window.read(timeout=200) #Refresh GUI
        s.connect((host, port)) # Begin connection
        window[f'-LED0-'].update(CIRCLE) # If connection, turn LED on
        #Transmit data for 50 iterations
        for iteration in range(1,51):
            jsondata = collate_data(iteration) #Grab the data
            if jsondata:
                event,values = window.read(timeout=200) #Refresh GUI
                if event == sg.WIN_CLOSED or event == 'Exit':
                    window.close()
                    break
                window[f'-LED0-'].update(CIRCLE) # if connection is still active keep LED on
                send_to_server(jsondata) # Send the data using by calling the send function
            time.sleep(2) # Send iterations and update GUI every 2 seconds
    except Exception: # If connection or server couldent be made/found
        window.read(timeout=200)#Refresh GUI
        window[f'-LED0-'].update(CIRCLE_OUTLINE) #Turn/keep Led off
        print("Couldent make a connection") #Print error statement

#Main Program
if __name__ == "__main__":
    try:
        vcgencmd_gui() #Run the main program
        # After 50 iterations of data close the socket and exit program
        s.close()
        print("Exiting...")
        exit()
    except Exception: # General program error catch
        print("Exiting...")
        s.close()
        exit()
    except KeyboardInterrupt: #CTRL-C to quit
        print("Exiting")
        exit()