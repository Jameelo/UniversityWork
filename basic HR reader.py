import machine
import utime

HR_PIN = 0
SAMPLE_INTERVAL = 0.05

HR_PPG = machine.ADC(HR_PIN)

while True:
    val = HR_PPG.read_u16()
    print("PPG data: ",val)
    utime.sleep(SAMPLE_INTERVAL)
