# This code will run on the base pc, and so can use python unrestricted.
# Retrieve heart data for processing, proof of concept for diagnostics.

import matplotlib.pyplot as plt
import numpy as np

def gTitleXY(Title,labelX,labelY):
    plt.title(Title) 
    plt.xlabel(labelX) 
    plt.ylabel(labelY) 

# Initialise y axis list
y = []

# Open data file
fileDest = open("J:\\University\\ACSEY4\\Project Work\\Data\\Serial_Data.txt","r")

# Load data into y axis variable
for line in fileDest:
    y.append(float(line)/(2**16))

fileDest.close()

# Timeseries section

# Create time axis for 256 samples & clip y values to the nearest power of 2 (for fft efficiency)
t = np.linspace(0,12.75,num=256)
yClip = y[0:256]

gTitleXY("Heart Data",'Samples','16-bit Light Intensity')
plt.yticks()
plt.plot(t,yClip)

plt.show()

# fft section

# calculate the fourier transform and the frequencies from the calculated bins
yFT = np.fft.fft(yClip)
f = np.fft.fftfreq(t.shape[-1],0.05)
yFTmag = []

for i,val in enumerate(yFT):
    yFTmag.append(np.linalg.norm(val))

gTitleXY("Fourier Transformed Heart Data",'Frequency buckets','Occurance') 
plt.plot(f,yFTmag)

plt.show()