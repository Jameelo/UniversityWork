"""
main for the device pico

take data samples at a rate of 20Hz, far over the bandwidth of the human heartrate.
Every 1200 entries (1 minute), save that data to an individual file.
Then every half hour, send 30 files over to the catcher pico to be sent to the "Server"


So the pseudocode is as follows:
Collect heart data @20Hz
Append it to a file
When the file has 1200 lines, close it and begin a new one
Repeat until there are 30 files
Then stop recording & transmit all 30 files to catcher pico.
After transmission, repeat from start.
"""

# Justify why the actual device is dumb with no signals processing!
# Mainly cuz it allows the pi to be replaced with a dedicated PCB at some point. FUTURE WORK

# Import in all necessary micropython modules
import machine
from utime import sleep