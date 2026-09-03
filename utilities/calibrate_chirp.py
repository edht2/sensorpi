""" Simple utility to help calibrate the chirp sensors """

import time  # Make sure time is imported at the top of your script
from app.sensors.Chirp.chirp_firmware import Chirp
from colorama import Fore

addr = input("Address of target sensor, eg. 0x20 (leave blank if you're not sure)\n>").strip().lower()
if addr == "": addr = "0x20"

addr = int(addr, 0)

try:
    chirp = Chirp(bus=1, address=addr)
    chirp.version
    
except PermissionError as pe:
    print(f"No Chirp device found! {Fore.YELLOW}hint: Check I²C is enabled! Use `raspi-config` to enable{Fore.RESET}")
    raise PermissionError

except IOError as ioe:
    print(f"No Chirp device found! {Fore.YELLOW}hint: Check you are probing the correct address. Use `i2cdetect -y 1` from i2c-tools library to probe all addresses{Fore.RESET}")
    raise IOError

# Read min moisture (Dry)
input("Ensure the sensor is completely dry then press enter")
chirp.trigger()
time.sleep(0.5)

dry_readings = []
for _ in range(10):
    val = chirp.moist
    if val is not False and val is not None:
        dry_readings.append(val)
    time.sleep(0.2)

min_moist = min(dry_readings) if dry_readings else "Error"

# Read max moisture (Wet)
input("Place the sensor in water, ensure it is submerged up to the black solder sleeve, then press enter")
chirp.trigger()
time.sleep(0.5)

wet_readings = []
for _ in range(10):
    val = chirp.moist
    if val is not False and val is not None:
        wet_readings.append(val)
    time.sleep(0.2)

max_moist = max(wet_readings) if wet_readings else "Error"

# Print the sensor readings range
print(f"Range: {min_moist} - {max_moist}\nAdd to `app/config.py`")
