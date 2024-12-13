# Max Molnar 100746162
# TPRG 2131 CRN 02 -Project 2
# Dec 11th, 2024

# ServerMM.py

# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

import socket
import os, time
import json
import PySimpleGUI as sg
import threading

# Setup socket parameters
s = socket.socket()
host = '10.0.0.225' #Local host or loopback address (for same machine)
port = 8000
s.bind((host, port))
s.listen(5)
print("Server Listening...")

# Accept connection and print host address
c, addr = s.accept()
print("Got connection from ", addr)


def receive_handler():
    '''Recieve and parse json data'''
    jsonReceived = c.recv(1024)
    data = json.loads(jsonReceived)
    return data

def refresh_gui(window, jsondata):
    '''Function to update the gui, blink LED'''
    ret1 = jsondata["Core Temperature"]
    window[f'-CoreTemp-'].update(ret1)
    ret2 = jsondata["Core Voltage"]
    window[f'-CoreVolt-'].update(ret2)
    ret3 = jsondata["Core Freq"]
    window[f'-CoreClock-'].update(ret3)
    ret4 = jsondata["RAM Voltage"]
    window[f'-voltRAM-'].update(ret4)
    ret5 = jsondata["GPU Mem"]
    window[f'-memGPU-'].update(ret5)
    ret6 = jsondata["Iteration"]
    window[f'-Iteration-'].update(ret6)
    
    #Blink LED twice when data is updated
    window[f'-LED0-'].update(CIRCLE)
    time.sleep(0.10)
    window[f'-LED0-'].update(CIRCLE_OUTLINE)
    time.sleep(0.10)
    window[f'-LED0-'].update(CIRCLE)
    time.sleep(0.10)
    window[f'-LED0-'].update(CIRCLE_OUTLINE)
    time.sleep(0.10)

CIRCLE = '\u2B24'
CIRCLE_OUTLINE = '\u25EF'


def main():
    '''Main program to start gui and run the second thread'''
    try:
        sg.theme('Light Blue')#Add colour to the GUI
        #Setup the layout, create spaces&keys for data to be updated
        layout = [[sg.Text('Incoming Data Display', font=('Helvetica', 16))],
                [sg.Text('Core Temperature:'), sg.Push(), sg.Text('', size=(20,1), key='-CoreTemp-'), sg.Push()],
                [sg.Text('Core Voltage:'), sg.Push(), sg.Text('', size=(20,1), key='-CoreVolt-'), sg.Push()],
                [sg.Text('Core Frequency:'), sg.Push(), sg.Text('', size=(20,1), key='-CoreClock-'), sg.Push()],
                [sg.Text('RAM Voltage:'), sg.Push(), sg.Text('', size=(20,1), key='-voltRAM-'), sg.Push()],
                [sg.Text('GPU Memory in Millions of Bytes:'), sg.Push(), sg.Text('', size=(20,1), key='-memGPU-'), sg.Push()],
                [sg.Text('Iteration Number:'), sg.Push(), sg.Text('', size=(20,1), key='-Iteration-'), sg.Push()],
                [sg.Text('Incoming data LED:', font=('Helvetica', 16))],
                [sg.Push(), sg.Text(CIRCLE_OUTLINE, text_color='Red', key='-LED0-'), sg.Push()],
                [sg.Button('Exit')]]
        
        window = sg.Window('Server Window - Max Molnar', layout, finalize=True)
        
        def recieve_thread(flag):
            '''Thread loop to handle the data receiving process'''
            try:
                while not flag.is_set():
                    json_data = receive_handler()
                
                    if json_data:
                        refresh_gui(window, json_data)
                    time.sleep(1.6)
            except Exception:
                print("Data transmit complete. ")
                exit()
        done_flag = threading.Event()       
        thread1 = threading.Thread(target=recieve_thread, args=(done_flag,))
        thread1.start()
        #Main loop for GUI
        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
        done_flag.set()
        thread1.join()
        print("Exiting...")
        window.close()
    except Exception:
        print("Error, Exiting...")
        exit()

if __name__ == "__main__":
     try:
        main()
        exit()
     except Exception:
         print("Error, Exiting...")
         exit()