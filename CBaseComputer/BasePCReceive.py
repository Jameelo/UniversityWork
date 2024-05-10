"""
Base PC program for long-term storage and processing of the collected health data.
This program acts as an analogue for a storage server in a real application.

Currently decided collection period: half an hour. (Might make it an hour if CSVs are smaller) [They aren't]

Interfaces with a Pico W (serial connection) to collect data.
Each collection period, the receiver pico receives (n) data files containing 1200 datapoints for each minute
This is then sent through a serial connection to this program.

Data to store, for each minute in a file of 1/2 hour:
Raw PPG if it's not an excessive amount of data (CALCULATE A DAYS WORTH OF DATA)
BPM from peak to peak detection (or modal frequency from fft between 1 and 3 (or 4) Hz)
HRV from standard deviation of inter-peak period (1/BPM)
"""

"""
Every minute, the device saves the recorded data into a text file. Pico capacity is around 800Kb
As this stores 1200 lines of 16-bit values, a single file will be (Worst case):
- 1200*18 = 19200 bits total (18 bits for the \r\n at the end, but lower values do make the string shorter)
- 19200 bits = 2400 bytes, so around 3 Kb per minute of data collected in the worst case.
- Storing a days worth of PPG data @20Hz is 11Mb. (Use the code in dev/test.py in dissertation!)
- This is a lot of data, can either not store PPG data, or can instead compress the data.
    - Compression might get style points.
"""

import serial
import serial.tools.list_ports
import time
import numpy

PICO_HARDWARE_ID = "2E8A:0005"              # Pico hardware ID to allow for dynamic connections
BAUDRATE = 115200                           # Serial baudrate
BASE_PATH = "data\\halfHour{}\\minute{}.txt"    # Dynamic filepath for health data


# def plotResults():
# def fourierAnalysis():
# def calcHRV(): # Get the hourly HRV from 1/bpm


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

while True:
    while not picoPort:    
        print("Unable to connect to Raspberry Pi Pico. Retrying connection...")
        picoPort = findPicoCOM() # COM port the pico is located in.
        time.sleep(3)

    print("Pico connected")

    serial_connection = serial.Serial(picoPort,BAUDRATE) # Establish connection with receiver pico

    # open file to store data in long-term. Aggregate into a CSV, storing hours as columns
    # format filepath here
    fileDest = open("J:\\University\\ACSEY4\\Project Work\\Data\\Serial_Data.txt","wb")

    # Now that the receiver pico has been connected, keep reading from it constantly until it gets unplugged
    while findPicoCOM():
        # Constantly look for an arbitrary "signal transmission" message
        # When this is found, begin receiving data and writing them to fileDest.
        # FileDest needs to be
        print(serial_connection)
        time.sleep(0.5)
        # dont forget to use ser.readline() to get the right length!!

    print("Connection lost")
    fileDest.close()
