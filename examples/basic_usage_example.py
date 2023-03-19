from time import sleep

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from HanmatekControl import HanmatekControl

hc = HanmatekControl()

hc.show()

hc.set_status(True)

for i in range(0, 7):
    sleep(1)
    #hc.set_power()
    hc.set_voltage(i)

hc.set_status(False)
hc.show()