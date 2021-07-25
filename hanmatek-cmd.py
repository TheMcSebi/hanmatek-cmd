#!/usr/bin/python3

import traceback
import minimalmodbus

#power_supply_port = "COM12" # windows
power_supply_port = "/dev/ttyUSB1" # linux

hanmatek=minimalmodbus.Instrument(power_supply_port, 1)    # port name, slave address
hanmatek.serial.baudrate=9600
hanmatek.serial.timeout=0.5
hanmatek.address = 1

is_powered_on = False
target_voltage = 0.0
target_current = 0.0

def read_data(display):
    value = hanmatek.read_registers(0x00, 0x33)
    
    if display:
        print("device power: " + str(bool(value[0x01])))
        
        #print("protectStat: " + str(value[0x02]))
        #print("overVoltageProtection: " + str(bool(value[0x02] & 0x01)))
        #print("overCurrentProtection: " + str(bool(value[0x02] & 0x02)))
        #print("overPowerProtection: " + str(bool(value[0x02] & 0x04)))
        #print("overTemperatureProtection: " + str(bool(value[0x02] & 0x08)))
        #print("shortCircuitProtection: " + str(bool(value[0x02] & 0x10)))

        #print("model: " + str( value[0x03]))
        #print("classDetail: " + str( value[0x04]))

        #print("decimals: " + str( value[0x05]))
        #print("decimalsVoltage: " + str( (value[0x05] >> 8) & 0x0F))
        #print("decimalsCurrent: " + str( (value[0x05] >> 4) & 0x0F))
        #print("decimalsPower: " + str( value[0x05] & 0x0F))

        print("current voltage: " + str( value[0x10] / 100))
        print("current current: " + str( value[0x11] / 1000))
        print("current power: " + str(((value[0x12] << 16) + value[0x13]) / 1000))
        #print("powerCal: " + str(value[0x14])) # ?

        #print("protectVoltage: " + str( value[0x20] / 100))
        #print("protectCurrent: " + str( value[0x21] / 1000))
        #print("protectPower: " + str( value[0x22]))
        
        print()
        print("target voltage: " + str( value[0x30] / 100))
        print("target current: " + str( value[0x31] / 1000))
        
        print()
    
    return [bool(value[0x01]), value[0x30] / 100, value[0x31] / 1000]

# currently unused
def read_limits():
    value = hanmatek.read_registers(0x1000, 0x05)
    
    print("mVoltage: " + str(value[0x00]))
    print("mCurrent: " + str(value[0x01]))
    print("mTimeSpan: " + str(value[0x02]))
    print("mEnable: " + str(value[0x03]))
    print("mNextOffset: " + str(value[0x04]))

# currently unused
def read_settings():
    value = hanmatek.read_registers(0xC110, 0x20)
    
    print("ul: " + str(value[0x00]))
    print("uh: " + str(value[0x0E]))
    print("il: " + str(value[0x10]))
    print("ih: " + str(value[0x1E]))

def set_voltage(val):
    global hanmatek
    try:
        hanmatek.write_register(0x30, round(val * 100))
    except:
        print(traceback.format_exc())

def set_current(val):
    global hanmatek
    try:
        hanmatek.write_register(0x31, round(val * 1000))
    except:
        print(traceback.format_exc())
    

def power_off():
    global hanmatek
    try:
        hanmatek.write_register(1, 0)
    except:
        print(traceback.format_exc())

def power_on():
    global hanmatek
    try:
        hanmatek.write_register(1, 1)
    except:
        print(traceback.format_exc())

def update_data(display):
    global is_powered_on, target_voltage, target_current
    data = read_data(display)
    is_powered_on = data[0]
    target_voltage = data[1]
    target_current = data[2]

update_data(True)
inp = "h"
while True:
    cmd = inp.split()
    
    if cmd[0] == "h" or cmd[0] == "?": # help
        print("command reference:")
        print("  h or ?         display this help text")
        print("  t              toggle power")
        print("  sv <float>     set voltage to <float>")
        print("  sc <float>     set current to <float>")
        print("  r              read current power supply configuration")
        print("  +[++] / -[--]  increase or decrease voltage")
        print("  q or x         exit")
        
    elif cmd[0] == "t": # toggle
        is_powered_on = not is_powered_on
        
        if is_powered_on:
            power_on()
        else:
            power_off()
    
    elif cmd[0] == "sv": # set voltage
        print("set voltage to " + cmd[1])
        set_voltage(float(cmd[1]))
    
    elif cmd[0] == "sc": # set current
        print("set current to " + cmd[1])
        set_current(float(cmd[1]))
    
    elif cmd[0] == "r": # read data
        update_data(True)
    
    elif cmd[0] == "q" or cmd[0] == "x": # quit
        print("quit")
        hanmatek.serial.close()
        exit()
    
    elif "+" in cmd[0]: # increase voltage
        update_data(False)
        strength = cmd[0].count("+")
        vadd = 10 ** strength / 1000
        target_voltage = target_voltage + vadd
        set_voltage(target_voltage)
        print("target voltage: " + str(round(target_voltage, 2)))
    
    elif "-" in cmd[0]: # decrease voltage
        update_data(False)
        strength = cmd[0].count("-")
        vadd = 10 ** strength / 1000
        target_voltage = target_voltage - vadd
        set_voltage(target_voltage)
        print("target voltage: " + str(round(target_voltage, 2)))
    
    else:
        print("unknown command, enter h or ? to display help")
    
    oldinp = inp
    inp = input("> ")
    if len(inp) == 0:
        inp = oldinp
