# RED CABLE (server), remove all print statements before shipping properly

from machine import Pin
import network
import random
import socket
import utime

LED = Pin("LED", Pin.OUT)
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]

def establishConnection():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NETWORK_PARAMS[0],NETWORK_PARAMS[1])

    # Verify created connection
    while not wlan.isconnected():
        print("waiting for connection...")
        utime.sleep(1)
    print("Connected to WiFi!")
    return wlan.ifconfig()[0]

def createSocket(ip):
    address = (ip,80)
    s = socket.socket()
    s.bind(address)
    s.listen(1)
    print("socket created")
    return s

# Connect to the hotspot and create a socket on port 80
hsIP = establishConnection()
receiverSocket = createSocket(hsIP)
client,cAddr = receiverSocket.accept()

while True:
    LED.value(1)
    req = client.read(2)
    if req == b'':
        client.close()
        LED.value(0)
        print("closing")
        break
    print(int.from_bytes(req,"little"))