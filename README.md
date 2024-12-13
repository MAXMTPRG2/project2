These two server and client programs are designed to work together to collate VCGENCMD command data from a raspberry pi and display it in a GUI. 
The file ClientMM.py grabs 5 different VCGENCMD data from the raspberry pi, converts it to JSON format and sends it as BYTE data in 50 iterations, in two second intervals, to the ServerMM.py program. 
It uses a PySimpleGUI to display a connection LED that will remain solid as long as there is a connection with the server and toggles every 2 seconds. 
If the connection with the server is lost, the program will immeaditley and smoothly shut down. After the 50 iterations of data are sent the program Exits.
The ClientMM.py file will only run on a Raspberry Pi, else it will immeaditley shutdown. 
The file ServerMM.py esablishes the socket and listens for a connection from the client. Once the connection is made a second thread is started, that handles the recieving process of the JSON data from the server
in 2 second intervals. Functions called within the second thread parse the data, and convert it to a usable dictionary that python can process; it then uses another function to update the data/display in a GUI. A PySimpleGUI is run in the main loop and is constantly updated/displays the recieved iterations
of VCGENCMD data from the server. The server GUI also has an LED that will blink twice anytime a new iteration of data is recieved by the server. Once all 50 iterations of data have been received and dispayed, the second thread ends and waits for an exit from
the main loop running the GUI. Both programs feature an Exit button in the GUI as a way to exit the program or the user can press CTRL-C to exit.
