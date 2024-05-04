# BLACK CABLE (device), remove all print statements before shipping properly

from machine import Pin
import network
import random
import socket
import utime

LED = Pin("LED", Pin.OUT)
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]

LED.value(0)

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

# Connect to the hotspot
hsIP = establishConnection()

serverInfo = socket.getaddrinfo(hsIP,80)
serverAddress = serverInfo[0][-1]
print(serverAddress)

senderSocket = socket.socket()
print("socket created")
senderSocket.connect(('192.168.176.80',80))

num = 1

while num < 17:
    LED.value(1)
    box = 2**num-1
    package = box.to_bytes(2,'little')
    senderSocket.send(package)
    #utime.sleep(0.5)
    num += 1

senderSocket.close()
LED.value(0)
print(0)
