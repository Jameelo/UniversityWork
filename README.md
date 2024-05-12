# Dissertaion project repo.
### The code here concerns the creation of an e-textiles platform that records and transmits heart data.

There are 3 separate machines used in this dissertation:
1. A Raspberry Pi Pico on a wearable device to collect heart PPG data over a 30 minute period, before wirelessly transmitting this data to the next device
2. A second Raspberry Pi Pico acting as a WiFi receiver, storing the received data and subsequently sending this data through a serial connection to the final device
3. A base storage computer which stores the data in the long-term and performs signals processing to extract the heart rate using the frequency domain, and the heart rate variability using the time domain.
