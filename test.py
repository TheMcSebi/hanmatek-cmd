from HanmatekControl import HanmatekControl
from time import sleep

hc = HanmatekControl()

hc.show()

hc.set_status(True)

for i in range(0, 7):
    sleep(1)
    #hc.set_power()
    hc.set_voltage(i)

hc.set_status(False)
hc.show()