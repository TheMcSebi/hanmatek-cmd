from HanmatekControl import HanmatekControl
from time import sleep
from os import system

hc = HanmatekControl(port="COM14")

while True:
    meter = hc.render_amp_meter(width=200)
    #system("cls")
    print(meter)
    sleep(0.5)