import os

PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\dummySD.txt"

MINUTES = 60

dFile = open(PATH,"wb")

# Simulates a worst-case size of a minute-long PPG file.
for n in range(1200):
    dFile.write(b"65536\r\n")

dFile.close()

manyFiles = os.path.getsize(PATH)/1024 * MINUTES

HOURFILE_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\dummyHourFile.txt"

dFile = open(HOURFILE_PATH,"wb")

for n in range(1200*MINUTES):
    dFile.write(b"65536\r\n")

dFile.close()

oneFile = os.path.getsize(HOURFILE_PATH)/1024

print(f"Many files: {manyFiles} \nOne file: {oneFile}")

minuteSize = os.path.getsize(PATH)/1024
hourSize = minuteSize * 60
daysize = hourSize * 24 / 1024 # Can sleep with device on

print(f"{minuteSize} Kb every minute \n{hourSize} Kb every hour \n{daysize} Mb every day")