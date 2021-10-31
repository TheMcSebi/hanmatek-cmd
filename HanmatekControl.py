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
        self._read()
    
    def _read(self):
        """
        Reads device registers.
        """
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
        """
        Set target voltage in Volts.
        
        :param val: Target voltage in Volts
        """
        try:
            self._hanmatek.write_register(0x30, round(float(val) * 100))
            self._read()
        except:
            raise RuntimeError(traceback.format_exc())

    def set_current(self, val):
        """
        Set current limit in Ampere.
        
        :param val: Current limit in Ampere
        """
        try:
            self._hanmatek.write_register(0x31, round(float(val) * 1000))
            self._read()
        except:
            raise RuntimeError(traceback.format_exc())
    
    def set_status(self, enabled = None):
        """
        Toggle device output on or off.
        
        :param enabled: Target device state. Toggled if omitted.
        """
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
    
    def get_status(self, cached = False):
        """
        Check if the device is currently enabled.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._status
    
    def get_power(self, cached = False):
        """
        Get current device power in Watts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._current_power
        
    def get_current(self, cached = False):
        """
        Get current current in Ampere.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._current_current

    def get_target_current(self, cached = False):
        """
        Get target current in Ampere.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._target_current

    def get_voltage(self, cached = False):
        """
        Get current voltage in Volts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._current_voltage

    def get_target_voltage(self, cached = False):
        """
        Get target voltage in Volts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        return self._target_voltage
    
    def show(self, cached = False):
        """
        Print various data from the device.

        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: self._read()
        print(f"output enabled: {self._status}\n")
        print(f"target voltage: {self._target_voltage} V")
        print(f"target current: {self._target_current} A\n")
        print(f"current voltage: {self._current_voltage} V")
        print(f"current current: {self._current_current} A")
        print(f"current power: {self._current_power} W")
    
    def print_amp_meter(self, current : float = None, width : int = 30):
        """
        :param current: value
        :param width: how many characters the display should be wide
        """
        if current == None:
            current = self.get_current()
        print(f"{current: >6} A: |", end="")
        maxnum = int(self._target_current*width)
        num = int(current/self._target_current*width)
        for i in range(0, num):
            print("#", end="")
        for i in range(0, maxnum-num):
            print(" ", end="")
        print("|")

    def sync_device(self):
        """
        Read device registers.
        """
        self._read()
        
    def __del__(self):
        self._hanmatek.serial.close()