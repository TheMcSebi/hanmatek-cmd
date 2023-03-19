import minimalmodbus
import traceback

class HanmatekControl:
    def __init__(self, port: str):
        self._hanmatek = None
        self._hanmatek = minimalmodbus.Instrument(port, 1)    # port name, slave address
        self._hanmatek.serial.baudrate = 9600
        self._hanmatek.serial.timeout = 0.5
        self._hanmatek.address = 1

        self._status = False
        self._target_voltage = 0.0
        self._target_current = 0.0
        self._current_voltage = 0.0
        self._current_current = 0.0
        self._current_power = 0.0
        self.sync_device()
    
    def sync_device(self) -> None:
        """
        Reads device registers.
        """
        value = self._hanmatek.read_registers(0x00, 0x33)

        # left unused registers in the code for future reference
        
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
        
        #print("target voltage: " + str( value[0x30] / 100))
        self._target_voltage = value[0x30] / 100
        
        #print("target current: " + str( value[0x31] / 1000))
        self._target_current = value[0x31] / 1000
    
    def set_voltage(self, value: float) -> None:
        """
        Set target voltage in Volts.
        
        :param val: Target voltage in Volts
        """
        if value < 0:
            raise ValueError("Voltage must be positive")
        
        try:
            self._hanmatek.write_register(0x30, round(float(value) * 100))
            self.sync_device()
        except:
            raise RuntimeError(traceback.format_exc())

    def set_current(self, value: float) -> None:
        """
        Set current limit in Ampere.
        
        :param val: Current limit in Ampere
        """
        if value < 0:
            raise ValueError("Current must be positive")
        
        try:
            self._hanmatek.write_register(0x31, round(float(value) * 1000))
            self.sync_device()
        except:
            raise RuntimeError(traceback.format_exc())
    
    def set_status(self, enabled: bool = None, cached: bool = False) -> None:
        """
        Toggle device output on or off.
        
        :param enabled: Target device state. Toggled if omitted.
        """
        if enabled is None: # if no value is provided, toggle the device
            if not cached: 
                self.sync_device()
            self._status = not self._status
        else:
            self._status = enabled
        
        try:
            self._hanmatek.write_register(0x01, int(self._status))
            self.sync_device()
        except:
            raise RuntimeError(traceback.format_exc())
    
    def get_status(self, cached: bool = False) -> bool:
        """
        Check if the device is currently enabled.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._status
    
    def get_power(self, cached: bool = False) -> float:
        """
        Get current device power in Watts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._current_power
        
    def get_current(self, cached: bool = False) -> float:
        """
        Get current current in Ampere.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._current_current

    def get_target_current(self, cached: bool = False) -> float:
        """
        Get target current in Ampere.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._target_current

    def get_voltage(self, cached: bool = False) -> float:
        """
        Get current voltage in Volts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._current_voltage

    def get_target_voltage(self, cached: bool = False) -> float:
        """
        Get target voltage in Volts.
        
        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        return self._target_voltage
    
    def show(self, cached: bool = False) -> float:
        """
        Print current device status.

        :param cached: skip device sync, useful when reading many values at once
        """
        if not cached: 
            self.sync_device()
        
        print(f"Device status: {'Enabled' if self._status else 'Disabled'}\n")
        print(f"Target voltage: {self._target_voltage} V")
        print(f"Target current: {self._target_current} A\n")
        print(f"Current voltage: {self._current_voltage} V")
        print(f"Current current: {self._current_current} A")
        print(f"Current power: {self._current_power} W")
    
    def render_amp_meter(self, current: float = None, power: float = None, voltage: float = None, width: int = 30) -> str:
        """
        Returns a string that displays the current device status as an amp meter.

        :param current/power/voltage: override values set on the device
        :param width: how many characters the display should be wide
        """
        if current is None:
            current = self.get_current()
        
        if power is None:
            power = self.get_power(True)
        
        if voltage is None:
            voltage = self.get_voltage(True)
        
        ret = f"{current: >6} A / {str(self._target_current) + 'A': <6} |"
        
        num = int((current/self._target_current)*width)
        for i in range(0, num):
            ret += "#"
        for i in range(0, width-num):
            ret += " "
        ret += f"| {power: >6} W  @ {voltage} V"

        return ret
        
    def __del__(self):
        if self._hanmatek is not None:
            self._hanmatek.serial.close()