# Dissertaion project repository
### The code here concerns the creation of an e-textiles platform that records and transmits heart data.

There are 3 separate machines used in this dissertation:
A. A Raspberry Pi Pico on a wearable device to collect heart PPG data over a 30 minute period, before wirelessly transmitting this data to the next device
B. A second Raspberry Pi Pico acting as a WiFi receiver, storing the received data and subsequently sending this data through a serial connection to the final device
C. A base storage computer which stores the data in the long-term and performs signals processing to extract the heart rate using the frequency domain, and the heart rate variability using the time domain.

Outside of folders A, B and C are supplementary programs used to either determine system features, or to learn about a specific concept relevant to the project requirements.
