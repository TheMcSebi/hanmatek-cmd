from time import sleep

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from HanmatekControl import HanmatekControl

hc = HanmatekControl(port="COM14")

while True:
    meter = hc.render_amp_meter(width=200)
    print(meter)
    sleep(0.5)