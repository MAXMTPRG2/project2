# Max Molnar 100746162
# TPRG 2131 CRN 02 -Project 2
# Dec 11th, 2024

# ClientMM.py

# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

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
    print("Not on a Raspberry Pi, Exiting...")
    exit()


# Setup socket object and parameters
s = socket.socket()
host = '10.0.0.225' # Local host of the Pi
port = 8000

def collate_data(iteration):
    '''Function to get/collate vcgencmd command data'''
    temp = float(subprocess.getoutput("vcgencmd measure_temp").split("=")[1].replace("'C", ""))
    voltage = float(subprocess.getoutput("vcgencmd measure_volts core").split("=")[1].replace("V", ""))
    clock = float(subprocess.getoutput("vcgencmd measure_clock core").split("=")[1])
    voltsram = float(subprocess.getoutput("vcgencmd measure_volts sdram_p").split("=")[1].replace("V", ""))
    memory = float(subprocess.getoutput("vcgencmd get_mem gpu").split("=")[1].replace("M", ""))
    
    data_dict = {"Core Temperature": round(temp,1), "Core Voltage": round(voltage,1), "Core Freq": round(clock,1),
                 "RAM Voltage": round(voltsram,1), "GPU Mem": round(memory,1), "Iteration": iteration}
    json_dict = json.dumps(data_dict)
    return json_dict

def send_to_server(jsonmessage):
    '''Function to send json data to the server'''
    jsonbyte = bytearray(jsonmessage, "UTF-8")
    s.send(jsonbyte)
    print("Data sent!")
    
    
def vcgencmd_gui():
    '''Main Function to handle GUI and Iterations 0 - 50'''
    sg.theme('Light Blue')
    
    CIRCLE = '\u2B24'              #  '⚫'
    CIRCLE_OUTLINE = '\u25EF'      #  '⚪'
    
    layout = [[sg.Text('Connection Indicator LED')],
            [sg.Push(), sg.Text(CIRCLE_OUTLINE, text_color='Red', key='-LED0-'), sg.Push()],
            [sg.Button('Exit')]]
    
    
    window = sg.Window('Client Window - Max Molnar', layout, font='Any 16')
    try:
        window.read(timeout=200)
        s.connect((host, port))
        window[f'-LED0-'].update(CIRCLE)
        #Transmit data for 50 iterations
        for iteration in range(1,51):
            jsondata = collate_data(iteration)
            if jsondata:
                event,values = window.read(timeout=200)
                if event == sg.WIN_CLOSED or event == 'Exit':
                    window.close()
                    break
                window[f'-LED0-'].update(CIRCLE)
                send_to_server(jsondata)
            time.sleep(2)
    except:
        window.read(timeout=200)
        window[f'-LED0-'].update(CIRCLE_OUTLINE)
        print("Couldent make a connection")

#Main Program
if __name__ == "__main__":
    try:
        vcgencmd_gui()
        s.close()
        print("Exiting...")
        exit()
    except Exception:
        print("Exiting...")
        s.close()
        exit()