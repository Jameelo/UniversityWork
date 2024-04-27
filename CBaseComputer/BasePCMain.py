"""
Base PC program for long-term storage and processing of the collected health data.
This program acts as an analogue for a storage server in a real application.

Currently decided collection period: half an hour. (Might make it an hour if CSVs are smaller) [They aren't]

Interfaces with a Pico W (serial connection) to collect data.
Each collection period, the receiver pico receives (n) data files containing 1200 datapoints for each minute
This is then sent through a serial connection to this program.

Data to store, for each minute in a file of 1/2 hour:
Raw PPG if it's not an excessive amount of data (CALCULATE A DAYS WORTH OF DATA)
BPM from peak to peak detection (or modal frequency from fft between 1 and 3 (or 4) Hz)
HRV from standard deviation of inter-peak period (1/BPM)
"""

"""
Every minute, the device saves the recorded data into a text file. Pico capacity is around 800Kb
As this stores 1200 lines of 16-bit values, a single file will be (Worst case):
- 1200*18 = 19200 bits total (18 bits for the \r\n at the end, but lower values do make the string shorter)
- 19200 bits = 2400 bytes, so around 3 Kb per minute of data collected in the worst case.
- Storing a days worth of PPG data @20Hz is 11Mb. (Use the code in dev/test.py in dissertation!)
- This is a lot of data, can either not store PPG data, or can instead compress the data.
    - Compression might get style points.
"""

# def plotResults():
# def fourierAnalysis():