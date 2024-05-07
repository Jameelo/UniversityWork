# main file for pico wirelessly receiving data, and sending it to the connected PC
"""
Receive data from the 30 files that are sent to the PC to be processed.
"""

from machine import Pin
import network
import socket
import utime

COLLECTION_PERIOD = 30                                 # Number of files the device records to before transmitting
BASE_PATH = "data/minute{}.txt"                 # Base path of data files
LED = Pin("LED", Pin.OUT)                       # Initialise LEDs
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]   # Network SSID and password for the AP.

LED.value(0)

"""
Function to connect to the wireless access point with the parameters defined in NETWORK_PARAMS.
Does not exit until a connection with the access point is established.
"""
def establishConnection():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NETWORK_PARAMS[0],NETWORK_PARAMS[1])
    # Verify created connection
    while not wlan.isconnected():
        utime.sleep(1)
    LED.value(1)
    return wlan.ifconfig()[0]

"""
Create the host socket
"""
def createSocket(ip):
    address = (ip,80)
    s = socket.socket()
    s.bind(address)
    s.listen(1)
    return s

"""
Send the received files to the base computer
"""
def sendStorage():
    for fileID in range(1,COLLECTION_PERIOD+1):
        # For every file
        filePath = BASE_PATH.format(fileID)
        curFile = open(filePath,"r")
        for line in curFile:
            print(line.encode())
        if fileID < COLLECTION_PERIOD:
            print("NewFi\r\n".encode())
        else:
            print("EndOT\r\n".encode())
    pass

receiverIP = establishConnection()
receiverSocket = createSocket(receiverIP)
LED.value(1)

sendStorage()

client,cAddr = receiverSocket.accept()

while True:
    client,cAddr = receiverSocket.accept() # Program stops here until a connection is established.
    minuteCount = 1
    filePath = BASE_PATH.format(minuteCount)
    writeFile = open(filePath,"wb")
    while True: # While a connection has been made (client will disconnect)
        packet = client.read(7)
        if packet.decode() == "NewFi\r\n": # signal for next file
            writeFile.close()
            minuteCount += 1
            filePath = BASE_PATH.format(minuteCount)
            writeFile = open(filePath,"wb")
            pass
        elif packet.decode() == "EndOT\r\n": # end of transmission
            writeFile.close()
            client.close()
            sendStorage()
            break
        elif packet == b'':
            # error
            writeFile.close()
            client.close()
            break
        else:
            writeFile.write(packet.decode())