# config
same_line = True
port = "COM12"

# import default libs
from time import sleep
import os, sys

# import HanmatekControl, search in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from HanmatekControl import HanmatekControl

# create instance of HanmatekControl
hc = HanmatekControl(port=port)

# continuously print the current output
while True:
    meter = hc.render_amp_meter(width=80)
    print(meter, end="\r" if same_line else "\n")
    sleep(0.5)