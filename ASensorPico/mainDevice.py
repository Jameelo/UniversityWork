"""
main program for the medical device's pico

take data samples at a rate of 20Hz, far over the bandwidth of the human heartrate.
Every 1200 entries minute, save that data to an individual file.
Then every half hour, send 30 files over to the catcher pico to be sent to the "Server".

Collect heart data @20Hz
Append it to a file
When the file has 1200 lines, close it and begin a new one
Repeat until there are 30 files
Then stop recording & transmit all 30 files to receiver pico.
After transmission, delete the 30 data files and repeat from start.
"""

# Justify why the actual device is dumb with no signals processing!
# Mainly as it allows the pi to be replaced with a dedicated PCB at some point. FUTURE WORK

# Import in all necessary micropython modules:
import machine
import network
import socket
import utime

# Numerical Constants
HR_PIN = 0                               # ADC pin for the PPG sensor
SAMPLE_INTERVAL = 0.05                   # Period between sample collection
SAMPLE_COUNT_MINUTE = 60/SAMPLE_INTERVAL # Number of samples collected in one minute
TIMEOUT_MAX_ATTEMPTS = 16                # Maximum number of attempts the program will make
COLLECTION_PERIOD = 30                   # Number of minutes the devices will collect data over before transmitting

BASE_PATH = "data\\minute{}.txt"                # Modular filepath for the data file
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]   # Network SSID and password for the hotspot.
SERVER_IP_PORT = ("192.168.176.80",80)          # IP of server host (receiver), and the open port

# Declare pins
HR_PPG = machine.ADC(HR_PIN)
LED = machine.Pin("LED", machine.Pin.OUT)

# Initialise LED to low
LED.value(0)


"""
Function to connect to the mobile hotspot with the parameters defined in NETWORK_PARAMS
"""
def establishConnection():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NETWORK_PARAMS[0],NETWORK_PARAMS[1])
    attempts = 0
    # Verify created connection
    while not wlan.isconnected() or attempts < TIMEOUT_MAX_ATTEMPTS:
        utime.sleep(1)
        attempts += 1
    return wlan.ifconfig()[0]

"""
Connect to the receiver and send all files over.
The socket magic happens here too.
At the end of the function, close all communication.
"""
def transmitFiles():
    # Create socket and connect to receiver
    sDevice = socket.socket()    
    sDevice.connect(SERVER_IP_PORT)
    # Then for each file: for fileID in range(COLLECTION_PERIOD):
        # Read a line
        # Send the size of the line in bytes
        # Then send the data
        # Repeat 1200 times until EOF
    # Close the socket & continue collection
    pass

# Main code begins below

minuteCount = 1
sampleCount = 0

filePath = BASE_PATH.format(minuteCount)
heartFile = open(filePath,"wb")

deviceIP = establishConnection()

while True:
    sampleCount += 1
    sPPG = HR_PPG.read_u16() # Sampled PPG reading
    heartFile.write(sPPG.to_bytes(2,'little')) # Store the sampled value into the text file

    if sampleCount >= SAMPLE_COUNT_MINUTE:
        sampleCount = 0
        minuteCount += 1
        if minuteCount > COLLECTION_PERIOD:
            sampleCount = 0
            minuteCount = 1
            # Send all 30 text files to the receiver pico, then delete them all.        
        # close current text file and open a new one with a name +1
        heartFile.close()
        filePath = BASE_PATH.format(minuteCount)
        heartFile = open(filePath,"wb")        

    utime.sleep(SAMPLE_INTERVAL)