"""
main program for the medical device's pico

take data samples at a rate of 20Hz, just over twice the bandwidth of the human heartrate.
Save recorded data to an individual file, one file for each minute recorded.
Then every half hour, send the 30 files over to the receiver pico to be sent to the storage device.
After transmission, the text files may be overwritten. The total storage occupied is around 300kb.
"""

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
TRANSMISSION_DELAY = 0.625               # Delay in seconds between sending each file, to give the receiver time to switch files.

# Filesystem and network constants
BASE_PATH = "data/minute{}.txt"                 # Modular filepath for the data file
NETWORK_PARAMS = ["PicoHotspot","RP2040_%^@"]   # Network SSID and password for the AP.
SERVER_IP_PORT = ("192.168.176.80",80)          # IP of server host (receiver), and the open port

# Declaration of pins
HR_PPG = machine.ADC(HR_PIN)
LED = machine.Pin("LED", machine.Pin.OUT)

# Initialise LED to low(off)
LED.value(0)


"""
Function to connect to the wireless access point with the parameters defined in NETWORK_PARAMS.
Attempt to connect up to TIMEOUT_MAX_ATTEMPTS times, before returning 0.
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
This function sends the entire contents of a single file.
It opens and manages its own socket as not to time out the connection in a long-lasting data transfer.
    This is a similar reason to why there are 30 text files.
"""
def sendSingle(fileID):
    # Open the socket
    sDevice = socket.socket()
    sDevice.connect(SERVER_IP_PORT)
    LED.value(1)

    # Begin reading the file
    filePath = BASE_PATH.format(fileID)
    curFile = open(filePath,"r")

    # Encode into UTF-8 and send to receiver
    for line in curFile:
        package = line.encode()
        sDevice.send(package)
        
    # Send an end of file or end of transmission statement?
    if fileID < COLLECTION_PERIOD:
        sDevice.send("NewFi\r\n".encode())
        utime.sleep(TRANSMISSION_DELAY)
    else:
        sDevice.send("EndOT\r\n".encode())

    # Close device and turn LED off
    sDevice.close()
    LED.value(0)
    return

"""
This function manages the transmission of all files to wirelessly send over to the receiver.
"""
def transmitFiles():    
    for fileID in range(1,COLLECTION_PERIOD+1): # For each file
        sendSingle(fileID)                      # Transmit file
    return


# Initialise counter variables
minuteCount = 1
sampleCount = 0

# Create initial file to write to (data/minute1.txt)
filePath = BASE_PATH.format(minuteCount)
heartFile = open(filePath,"wb")

# Connect to the access point, or continue to attempt to connect to the access point until a connection is made.
deviceIP = establishConnection()

while True:
    sampleCount += 1
    sPPG = HR_PPG.read_u16() # Sampled PPG reading
    heartFile.write(sPPG.to_bytes(2,'little')) # Store the sampled value into the text file

    if sampleCount >= SAMPLE_COUNT_MINUTE:
        minuteCount += 1
        sampleCount = 0
        if minuteCount > COLLECTION_PERIOD:
            minuteCount = 1
            sampleCount = 0
            # Send all 30 text files to the receiver pico 
            transmitFiles()
        # close current text file and open a new one with a name +1
        heartFile.close()
        filePath = BASE_PATH.format(minuteCount)
        heartFile = open(filePath,"wb")        

    utime.sleep(SAMPLE_INTERVAL)
