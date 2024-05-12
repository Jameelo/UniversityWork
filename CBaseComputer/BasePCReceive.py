"""
Base PC program for long-term storage and processing of the collected health data.
This program acts as an analogue for a storage server in a real application.

Interfaces with a Pico W (serial connection) to collect data.
Each collection period, the receiver pico receives (n) data files containing 1200 datapoints for each minute
This is then sent through a serial connection to this program.
"""

import serial
import serial.tools.list_ports
import time
import os

PICO_HARDWARE_ID = "2E8A:0005"              # Pico hardware ID to allow for dynamic connections
BAUDRATE = 115200                           # Serial baudrate
BASE_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\HeartData\\halfHour{}\\minute{}.txt"    # Dynamic filepath for health data

"""
Check to see if a device containing the Raspberry Pi Pico's hardware ID is connected to this device.
"""
def findPicoCOM():
    portList = serial.tools.list_ports.comports()
    for portData in portList:
        port,_,hwid = portData
        if PICO_HARDWARE_ID in hwid:
            return port
    return ""

picoPort = findPicoCOM()

halfHourCount = 1
minutecount = 1

while True:
    while not picoPort:    
        print("Unable to connect to Raspberry Pi Pico. Retrying connection...")
        picoPort = findPicoCOM() # COM port the pico is located in.
        time.sleep(1)

    print("Pico connected")

    filePath = BASE_PATH.format(halfHourCount,minutecount)
    if not os.path.exists(filePath):
        os.makedirs(filePath[:-14])
    fileDest = open(filePath,"w")

    serial_connection = serial.Serial(picoPort,BAUDRATE) # Establish connection with receiver pico

    # Now that the receiver pico has been connected, keep reading from it constantly until it gets unplugged
    while True:
        if findPicoCOM():
            serData = serial_connection.readline()
        if serData != b'' and serData != b'\r\n':
            # Then the received data is not empty, and should be written to a file.
            data = serData.decode()
            if "NewFi" in data: # If the program is to write to a new file    
                minutecount += 1
                filePath = BASE_PATH.format(halfHourCount,minutecount)
                fileDest = open(filePath,"w")
            elif "EndOT" in data: 
                # If the transmission has ended
                halfHourCount += 1
                minutecount = 0 
                fileDest.close()
                break
            else:
                # Otherwise, the recieved data must be numerical.
                fileDest.write(data)
    time.sleep(5)
