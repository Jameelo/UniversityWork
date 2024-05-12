import numpy as np
import matplotlib.pyplot as plt

# Stuff from half-hourly analysis:
#   HRV can be taken as a half hourly mertic
#   also can do a moving average filter to clean the data up.

BASE_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\HeartData\\halfHour{}\\minute{}.txt"    # Dynamic filepath for health data
COLLECTION_PERIOD = 30 # Number of minute files generated over the collection period
FREQUENCY_LOWER_BOUND = 40
FREQUENCY_UPPER_BOUND = 216
MOVING_AVERAGE_KERNEL = np.ones(5)/5 
PPG_RESOLUTION_MS = 50 # Resolution of PPG readings in ms
TIME_ANALYSIS_THRESHOLD = 0.503 # Heartbreat Detection Threshold

halfHour = 1
minuteFile = 1

"""
Function that uses the fourier transform to determine heart rate
"""
def getHeartRate(dataFT,freqBins):
    # Get the modal frequency between 0.6 and 3.6Hz
    modFreqInd = np.argmax(dataFT[FREQUENCY_LOWER_BOUND:FREQUENCY_UPPER_BOUND])
    modalFreq = freqBins[modFreqInd+FREQUENCY_LOWER_BOUND]
    return modalFreq * 60

"""
Function that uses time domain analysis to determine heart rate variability.
Standard deviation of RR intervals over the entire minute.
"""
def getHeartRateVariability(minuteData):   
    RRintArray = []
    BTimeArray = [0]

    # Generate values for ALL threshold intervals
    for n,val in enumerate(minuteData):
        if val > TIME_ANALYSIS_THRESHOLD and n-BTimeArray[-1] > 7:
            # If the value is large enough to count as a heartbeat, and it has been at least .35 seconds
            if minuteData[n-1] < val and minuteData[n+1] < val:
                # If the point is a local maximum
                RRinterval = (n-BTimeArray[-1])*20 # This value is the RR interval in units of 1/20th of a second.
                RRintArray.append(RRinterval)
                BTimeArray.append(n)

    HRVar = np.std(RRintArray)

    return int(HRVar)

"""
Function to calculate the fourier transform and their respective frequencies.
"""
def fourierTransform(data,t):
    yFT = np.fft.fft(data)    
    yFTmag = [] # Array to store FFT magnitude in.
    for val in yFT:
        yFTmag.append(np.linalg.norm(val))
    return yFTmag

"""
Produce a plot with titles.
"""
def plotGraph(xAxis,yAxis,xTitle,yTitle,mainTitle):
    plt.title(mainTitle) 
    plt.xlabel(xTitle) 
    plt.ylabel(yTitle)    
    plt.plot(xAxis,yAxis)

"""
Unpack a PPG minute file into an array and return it.
"""
def unpackMinute(minuteID,halfHourID):
    minuteArray = np.zeros(1200)
    filePath = BASE_PATH.format(halfHourID,minuteID)
    dataFile = open(filePath,"r")
    for index,line in enumerate(dataFile):
        minuteArray[index] = float(line)/(2**16)
    return minuteArray

"""
Function to write heart rate and heart rate variability data to
"""
def writeToFile(halfHourID,HRdata,HRVdata):
    filePath = BASE_PATH[:-13] + "\\HeartStats.txt"
    filePath = filePath.format(halfHourID)
    print("Processed data file can be found at: ",filePath)
    dataFile = open(filePath,"w")
    dataFile.write("Heart Rate, Heart Rate Variability\r\n")
    for index in range(0,COLLECTION_PERIOD-1):
        dataFile.write("{},{}\r\n".format(HRdata[index],HRVdata[index]))
        pass
    dataFile.close()

# Initialise arrays to save memory
halfHourPlotHR = np.zeros(30)
halfHourPlotHRV = np.zeros(30)
wholeHalfHour = np.zeros(1200*30)
timeArr = np.linspace(0,60,num=1200)
freqArr = np.fft.fftfreq(timeArr.shape[-1],0.05) # By inserting 0.05 seconds into this function, the frequency buckets will be plotted as Hz.

for minute in range(1,COLLECTION_PERIOD+1): # For each minute in the half hour period
    minData = unpackMinute(minute,halfHour)        # Unpack that minute into an array
    minData = np.convolve(minData, MOVING_AVERAGE_KERNEL, mode='same') # Clean this data using a moving average filter.
    minDataFT = fourierTransform(minData,timeArr)
    heartRate = getHeartRate(minDataFT,freqArr)
    wholeHalfHour[(minute-1)*1200:minute*1200] = minData
    heartRateVariability = getHeartRateVariability(minData)
    halfHourPlotHR[minute-1] = heartRate
    halfHourPlotHRV[minute-1] = heartRateVariability
    # plt.subplot(2,1,1)
    # plotGraph(timeArr,minData,"Time (s)","16-bit Light Intensity","Timeseries plot of heart rate.")
    # plt.plot(timeArr,np.ones(1200)*TIME_ANALYSIS_THRESHOLD)
    # plt.subplot(2,1,2)
    # plotGraph(freqArr[1:250],minDataFT[1:250],"Frequency (Hz)","Magnitude","Frequency Domain plot of heart rate.")
    # plt.show()

plt.subplot(2,1,1)
plotGraph(np.linspace(0,30,num=30),halfHourPlotHR,"Time (Minutes)","Heart Rate (BPM)","Plot of heart rate over time")
plt.subplot(2,1,2)
plotGraph(np.linspace(0,30,num=30),halfHourPlotHRV,"Time (Minutes)","Heart Rate Variability (ms)","Plot of heart rate variability")
plt.suptitle("Minutely heart rate and heart rate variability over a 30 minute period")
plt.show()

writeToFile(halfHour,halfHourPlotHR,halfHourPlotHRV)