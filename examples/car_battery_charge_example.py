import os, sys
from time import sleep
import signal

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from HanmatekControl import HanmatekControl

# Charge a 12V lead-acid car battery until it's almost full.
#
# Charging strategy (constant-current / constant-voltage):
#   1. Bulk phase  – charge at a steady current until the battery voltage
#                    reaches the absorption voltage (14.4 V).
#   2. Absorption  – hold voltage at 14.4 V while current tapers.
#                    Stop when the current drops below a small threshold,
#                    indicating the battery is nearly full.
#
# Adjust the constants below to match your battery and charger capacity.

CHARGE_VOLTAGE = 14.4       # absorption voltage (V)
CHARGE_CURRENT = 2.0        # bulk charge current limit (A)
FULL_CURRENT_THRESHOLD = 0.15  # stop when current drops below this (A)
PORT = "COM5"

hc = HanmatekControl(port=PORT)
hc.set_status(False)

def shutdown(sig=None, frame=None):
    print("\nshutting down, disabling output...")
    hc.set_status(False)
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

input("Connect the battery and press Enter to start charging")

print(f"charging at {CHARGE_VOLTAGE} V / {CHARGE_CURRENT} A limit")
hc.set_voltage(CHARGE_VOLTAGE)
hc.set_current(CHARGE_CURRENT)
hc.set_status(True)

try:
    while True:
        hc.sync_device()
        voltage = hc.get_voltage(cached=True)
        current = hc.get_current(cached=True)

        print(hc.render_amp_meter(current, voltage=voltage), end="\r")

        # Once the battery reaches absorption voltage the PSU switches from
        # constant-current to constant-voltage automatically. When the charge
        # current tapers below the threshold the battery is nearly full.
        if voltage >= CHARGE_VOLTAGE - 0.05 and current < FULL_CURRENT_THRESHOLD:
            break

        sleep(2)

    print(f"\nbattery nearly full (current tapered to {current:.2f} A)")
finally:
    hc.set_status(False)
    print("output disabled – remove the battery")
