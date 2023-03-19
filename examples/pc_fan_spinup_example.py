from HanmatekControl import HanmatekControl
from time import sleep, time
import signal
import sys

# make a server fan start up at a higher voltage
# when it's spun up, lower the voltage to limit its speed (and noise level)



sleep_time = 900
spinup_voltage = 8
current_limit = 1.3
continuous_voltage = 5.5

hc = HanmatekControl(port="COM10")
hc.set_status(False)

def signal_handler(sig, frame):
    hc.set_status(False)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

inp = input("Enter to continue")

print(f"setting voltage to {spinup_voltage}v, current limit to {current_limit}a")
hc.set_voltage(spinup_voltage)
hc.set_current(current_limit)
#inp = input("8v/1.1A\nEnter to continue")
hc.set_status(True)
print("supply enabled. waiting for spinup...")

current = 0
while current < current_limit*0.85:
    current = hc.get_current()
    print(hc.render_amp_meter(current), end="\r")
    sleep(0.1)

print(f"\nfans spun up, lowering voltage, idle for {sleep_time/60} minutes")

hc.set_voltage(continuous_voltage)

sleep_until = time() + sleep_time
while time() < sleep_until:
#for i in range(0, 10):
    current = hc.get_current()
    print(hc.render_amp_meter(current), end="\r")
    sleep(0.1)


sleep(sleep_time)
hc.set_status(False)