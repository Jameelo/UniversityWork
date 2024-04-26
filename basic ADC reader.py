import machine
import utime

band = machine.ADC(0)

while True:
    val = band.read_u16()
    print(val)
    utime.sleep(0.1)