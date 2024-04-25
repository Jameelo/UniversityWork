# This program runs on a dedicated storage pc to store recieved data.

import serial
import serial.tools.list_ports

PICO_HARDWARE_ID = "2E8A:0005"

def findPicoCOM():
    picoPort = ""
    portList = serial.tools.list_ports.comports()
    for port in portList:
        port,_,hwid = port
        if PICO_HARDWARE_ID in hwid:
            # connect to it here
            picoPort = port
    return picoPort

port = findPicoCOM() # COM port the pico is located in.

if port:
    baudrate = 115200
    serial_connection = serial.Serial(port,baudrate)

    # open file
    fileDest = open("J:\\University\\ACSEY4\\Project Work\\Data\\Serial_Data.txt","wb")

    while True:
        data = serial_connection.read(7)
        print(data)
        if data >= b"60000":
            print(data)
            break
        fileDest.write(data)

    fileDest.close()
    serial_connection.close()
else:
    print("Invalid pico COM port, program could not be run.")