import serial.tools.list_ports

PICO_HARDWARE_ID = "2E8A:0005"

portList = serial.tools.list_ports.comports()

for port in portList:
    port,desc,hwid = port
    if PICO_HARDWARE_ID in hwid:
        # connect to it here
        print(port)
    else:
        print(0)

# When serial.tools.list_ports.comports() is used to retrieve data from all devices occupying a COM port, there is a field called hwid, or hardware ID.
# This string contains a value named VID:PID, or vendor and product ID respectively.
# Below is an example of a raspberry pi pico's hwid:
# USB VID:PID=2E8A:0005 SER=E6614C311B336D31 LOCATION=1-2:x.0
# The left half (2E8A) means that the connected product is a raspberry pi product.
# The right half (0005) indicates that the product is a raspberry pi pico running micropython firmware.
# If the product can be confirmed to be a raspberry pi pico running micropython, then its corresponding COM port is the one that needs to be connected to.
# This saves needing to use thonny to find which com port the pico is connected to, and instead making it dynamic.