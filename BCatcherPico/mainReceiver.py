# main file for pico wirelessly receiving data, and sending it to the connected PC
"""
Receive data from the 30 files that are sent to the PC to be processed.
"""

from machine import Pin
import network
import socket
import utime
import serial

LED = Pin("LED", Pin.OUT)
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]

LED.value(0)

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

receiverIP = establishConnection()
receiverSocket = createSocket(receiverIP)

while True:
    client,cAddr = receiverSocket.accept() # Program stops here until a connection is established.

    # When a connection is establish, recieve a package saying the size of the data being sent
    # Using this, receive the heart data snippet
    # Then send that packet of heart data over serial (print statement)

# Receive data here
# Data recieved is a text file
# This is done by Wi-Fi/Bluetooth.
# Program should be able to detect when a connection is established.

# Send data here
# This is done by serial connection.
# Will need to ensure all packets have the same size, or just send them with delimiters.