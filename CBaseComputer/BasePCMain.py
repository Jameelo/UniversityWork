"""
Base PC program for long-term storage of the collected health data.
This program acts as an analogue for a storage server in a real application.

Interfaces with a Pico W to allow wireless data transmission from the device.
Each hour, receive 60 data entries containing 1200 datapoints

Data to
"""

"""
Every minute, the device saves the recorded data into a text file. Pico capacity is around 800Kb
As this stores 1200 lines of 16-bit values, a single file will be (Worst case):
- 1200*18 = 19200 bits total (18 bits for the \r\n at the end, but lower values do make the string shorter)
- 19200 bits = 2400 bytes, so around 3 Kb per minute of data collected in the worst case.
- 
"""

# def plotResults():
# def fourierAnalysis():