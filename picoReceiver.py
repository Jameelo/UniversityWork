import serial
import serial.tools.list_ports

PICO_HARDWARE_ID = "2E8A:0005"
BAUDRATE = 115200

def findPicoCOM():
    portList = serial.tools.list_ports.comports()
    for portData in portList:
        port,_,hwid = portData
        if PICO_HARDWARE_ID in hwid:
            return port
    return ""

port = findPicoCOM() # COM port the pico is located in.

if port:
    serial_connection = serial.Serial(port,BAUDRATE)

    # open file
    fileDest = open("J:\\University\\ACSEY4\\Project Work\\Data\\Serial_Data.txt","wb")

    while True:
        data = serial_connection.read(7)
        print(data)
        # The real data is sent periodically so there will be a clear EOT character.
        if data >= b"60000":
            print(data)
            break
        fileDest.write(data)

    fileDest.close()
    serial_connection.close()

    # Plot results
else:
    print("Invalid pico COM port, program could not be run.")