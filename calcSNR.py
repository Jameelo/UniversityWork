# This program takes in noise & signal data, and calculates the sigal:noise ratio, and also gets the value in dB
# The purpose of this program caved in a bit, as it now graphs fourier transforms.
import numpy as np
import matplotlib.pyplot as plt

SIGNAL_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\RecievedData\\data\\minute1.txt"
NOISE_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\NoiseExp\\THREAD_TEST_NOISE_PPG.txt"
COMPARE_PATH = "J:\\University\\ACSEY4\\Project Work\\Data\\LocationExp\\TopWristPPG.txt"

SAMPLE_INTERVAL = 0.05

"""
Calculate the power of a signal
"""
def signalPower(signal):
    seriesLength = len(signal)

    energySum = 0

    for n in range(seriesLength):
        energySum += signal[n]*signal[n]

    return energySum/seriesLength


"""
Function to quickly add the title & axis labels to a plot
"""
def gTitleXY(Title,labelX,labelY):
    plt.title(Title) 
    plt.xlabel(labelX) 
    plt.ylabel(labelY) 

"""
Function to take in a text file and return a normalised (from 16 bit) float array
"""
def unpackFile(fIn):
    data = []    
    for line in fIn:
        data.append(int(line)/(2**16))
    return data

"""
Calculate the fourier transform of a signal.
"""
def fourierTransform(signal):
    signalFT = np.fft.fft(signal)

    signalFTmag = []
    for val in signalFT:
        signalFTmag.append(np.linalg.norm(val))
    
    return signalFTmag

"""
Create a function to clip frequency data symmetrically
"""
def clipFreqData(data,freq,maxVal):
    minVal = maxVal *-1
    cutoffPos = 0
    cutoffNeg = 0

    # Count array bounds
    for i,n in enumerate(freq):
        if i < 256:
            # Positive indices
            if n >= maxVal and cutoffPos == 0:
                cutoffPos = i
        else:
            # Negative indices
            if n >= minVal and cutoffNeg == 0:
                cutoffNeg = i

    newDataPos = data[:cutoffPos]
    newDataNeg = data[cutoffNeg:]

    newData = np.concatenate((newDataNeg,newDataPos))

    newFreqPos = freq[:cutoffPos]
    newFreqNeg = freq[cutoffNeg:]

    newFreq = np.concatenate((newFreqNeg,newFreqPos))
    
    print(cutoffPos,cutoffNeg,len(freq),len(data),len(newFreq),len(newData))

    return newFreq,newData
    
"""
Function that uses the fourier transform to determine heart rate
"""
def getHeartRate(dataFT,freqBins):
    # Get the modal frequency between 0.6 and 3.6Hz
    pass

# Unpack both files
signalFile = open(SIGNAL_PATH,"r")
sData = unpackFile(signalFile)
signalFile.close()
sData = sData[:417]

compareFile = open(COMPARE_PATH,"r")
cData = unpackFile(compareFile)
compareFile.close()
cData = sData[:417]

noiseFile = open(NOISE_PATH,"r")
nData = unpackFile(noiseFile)
noiseFile.close()

# Create time array
lineCount = len(sData)
endTime = lineCount*SAMPLE_INTERVAL # Caclulate the length of data collection
timeArray = np.linspace(0,endTime,num=lineCount)

# Calculate signal powers
powerSignal = signalPower(sData)
powerNoise = signalPower(nData)

# Calculate the SNR in dB
snrDb = 10*np.log10(powerSignal/powerNoise)

print("Time domain calculation: ",snrDb)

# Calculate fourier transform of signals
f = np.fft.fftfreq(timeArray.shape[-1],SAMPLE_INTERVAL)

signalFT = fourierTransform(sData)
noiseFT = fourierTransform(nData)
compareFT = fourierTransform(cData)

# fClipS,signalFT = clipFreqData(signalFT,f,5)
# fClipN,noiseFT = clipFreqData(noiseFT,f,5)

powerSignalFT = signalPower(signalFT)
powerNoiseFT = signalPower(noiseFT)

# Calculate the SNR in dB
snrDb = 10*np.log10(powerSignalFT/powerNoiseFT)

print("Frequency domain calculation: ",snrDb)

plt.subplot(2, 2, 1)
plt.plot(timeArray,sData)
gTitleXY("Time domain Transmitted Signal",'Time','16-bit Magnitude') 

# plt.subplot(2, 2, 2)
# plt.plot(timeArray,nData)
# gTitleXY("Time domain PPG Noise",'Time','16-bit Magnitude') 

plt.subplot(2, 2, 2)
plt.plot(f,signalFT)
gTitleXY("Frequency domain Transmitted Signal",'Frequency','Magnitude') 

# plt.subplot(2, 2, 4)
# plt.plot(f,noiseFT)
# gTitleXY("Frequency domain PPG Noise",'Frequency','Magnitude') 

plt.subplot(2, 2, 3)
plt.plot(timeArray,cData)
gTitleXY("Time domain Reference Signal",'Time','16-bit Magnitude') 

plt.subplot(2, 2, 4)
plt.plot(f,compareFT)
gTitleXY("Frequency domain Reference Signal",'Frequency','Magnitude') 

plt.suptitle("PPG collected from top of wrist")
plt.show()