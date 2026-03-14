import os, sys, csv
from time import sleep
from datetime import datetime

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

log_path = os.path.join(os.path.dirname(__file__), f"charge_log_{datetime.now():%Y%m%d_%H%M%S}.csv")
log_file = open(log_path, "w", newline="")
log_writer = csv.writer(log_file)
log_writer.writerow(["timestamp", "voltage", "current", "power"])

print(f"charging at {CHARGE_VOLTAGE} V / {CHARGE_CURRENT} A limit")
print(f"logging to {log_path}")
hc.set_voltage(CHARGE_VOLTAGE)
hc.set_current(CHARGE_CURRENT)
hc.set_status(True)

try:
    while True:
        hc.sync_device()
        voltage = hc.get_voltage(cached=True)
        current = hc.get_current(cached=True)
        power = hc.get_power(cached=True)

        log_writer.writerow([datetime.now().isoformat(), voltage, current, power])
        log_file.flush()

        print(hc.render_amp_meter(current, voltage=voltage), end="\r")

        # Once the battery reaches absorption voltage the PSU switches from
        # constant-current to constant-voltage automatically. When the charge
        # current tapers below the threshold the battery is nearly full.
        if voltage >= CHARGE_VOLTAGE - 0.05 and current < FULL_CURRENT_THRESHOLD:
            break

        sleep(2)

    print(f"\nbattery nearly full (current tapered to {current:.2f} A)")
    print("output left enabled - disconnect manually when ready")

    while True:
        print("\a", end="", flush=True)
        sleep(1)

except KeyboardInterrupt:
    print("\ninterrupted - output left enabled, disconnect manually")
finally:
    log_file.close()
