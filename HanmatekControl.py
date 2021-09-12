import minimalmodbus
import traceback

class HanmatekControl:
    def __init__(self, port : str = "/dev/ttyUSB0"):
        self._hanmatek=minimalmodbus.Instrument(port, 1)    # port name, slave address
        self._hanmatek.serial.baudrate=9600
        self._hanmatek.serial.timeout=0.5
        self._hanmatek.address = 1

        self._status = False
        self._target_voltage = 0.0
        self._target_current = 0.0
        self._current_voltage = 0.0
        self._current_current = 0.0
        self._current_power = 0.0
    
    def _read(self, display = False):
        value = self._hanmatek.read_registers(0x00, 0x33)
        
        #print("device power: " + str(bool(value[0x01])))
        self._status = bool(value[0x01])
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

        #print("current voltage: " + str( value[0x10] / 100) + "V")
        self._current_voltage = value[0x10] / 100

        #print("current current: " + str( value[0x11] / 1000) + "A")
        self._current_current = value[0x11] / 1000
        
        #print("current power: " + str(((value[0x12] << 16) + value[0x13]) / 1000) + "W")
        self._current_power = ((value[0x12] << 16) + value[0x13]) / 1000

        #print("powerCal: " + str(value[0x14])) # ?

        #print("protectVoltage: " + str( value[0x20] / 100))
        #print("protectCurrent: " + str( value[0x21] / 1000))
        #print("protectPower: " + str( value[0x22]))
        
        #print()
        #print("target voltage: " + str( value[0x30] / 100))
        self._target_voltage = value[0x30] / 100
        
        #print("target current: " + str( value[0x31] / 1000))
        self._target_current = value[0x31] / 1000
        
        #print()
        
        #data = read_data(display)
        
        
        #return [bool(value[0x01]), value[0x30] / 100, value[0x31] / 1000] # [power status, voltage, current]
        return (value[0x12] << 16) + value[0x13]
    
    def set_voltage(self, val):
        try:
            self._hanmatek.write_register(0x30, round(float(val) * 100))
            self._read()
        except:
            raise RuntimeError(traceback.format_exc())

    def set_current(self, val):
        
        try:
            self._hanmatek.write_register(0x31, round(float(val) * 1000))
            self._read()
        except:
            raise RuntimeError(traceback.format_exc())
    
    def set_status(self, enabled = None):
        if enabled == None: # if no value is provided, toggle the device
            if self._status:
                enabled = False
            else:
                enabled = True
        else:
            enabled = bool(enabled)

        try:
            self._hanmatek.write_register(1, int(enabled))
            self._read()
        except:
            raise RuntimeError(traceback.format_exc())
    
    def get_status(self):
        self._read()
        return self._status
    
    def get_power(self):
        self._read()
        return self._current_power
        
    def get_current(self):
        self._read()
        return self._current_current

    def get_voltage(self):
        self._read()
        return self._current_voltage
    
    def show(self):
        self._read()
        print(f"output enabled: {self._status}\n")
        print(f"target voltage: {self._target_voltage}")
        print(f"target current: {self._target_current}\n")
        print(f"current voltage: {self._current_voltage}")
        print(f"current current: {self._current_current}")
        print(f"current power: {self._current_power}")
        
    def __del__(self):
        self._hanmatek.serial.close()