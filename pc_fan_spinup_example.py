from HanmatekControl import HanmatekControl
from time import sleep

# make a server fan start at a higher voltage
# when it's spinning, lower the voltage to limit its speed

hc = HanmatekControl(port="COM13")

print("setting voltage to 8v, current limit to 1a")
hc.set_voltage(8)
hc.set_current(1)
hc.set_status(True)
print("supply enabled. waiting for spinup...")

current = 0
while current < 0.6:
    current = hc.get_current()
    hc.print_amp_meter(current)
    sleep(0.1)

print("fans booted up, lowering voltage")
hc.set_voltage(4.6)
print("finished.")

for i in range(0, 50):
    current = hc.get_current()
    hc.print_amp_meter(current)
    sleep(0.1)