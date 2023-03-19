# Hanmatek-Cmd
Python implementation for to interactiv control of a Hanmatek bench power supply
The minimalmodbus library is used to read and write data over the power supplies USB interface.

For a [library version](#lib_ver_), see below.

## Installation
Install the minimalmodbus library by running `pip -r requirements.txt`.
On Linux you may also need to grant permission to your user to use the serial interface (/dev/ttyUSB0 in my case).
To do this, add the group "dailup" to your linux user account and restart your shell.

## Usage
Execute `python HanmatekCmd.py`

You can either specify the serial port by appending ` --port COM5` or ` --port /dev/ttyUSB0`, or after starting the shell by typing `port COM5` or `port /dev/ttyUSB0`. This change is not persistent though


    h or ?           display this help text
    ports            list available serial ports
    port             change serial port
    t                toggle power
    sv <float>       set voltage to <float>
    sc <float>       set current to <float>
    r                read and display current status
    +[++] / -[--]    increase or decrease voltage
    q or x           exit


If no new input is provided and the enter button is pressed, the previous command will be repeated. This makes it easy to step the voltage up or down continuously.  

Voltage and current can also be input directly by postfixing the input value with "a" for ampere and "v" for volt, e.g. `4.2v`.  

The increment and decrement commands support an optional multiplier, e.g. `++4` increases the voltage by 0.4V.  

### Example usage

* Running the script: `python HanmatekCmd.py --port COM5`
* Setting voltage to 3.3 V: `sv 3.3`
* Setting current limiter to 0.2 A: `sc 0.2`
* Turn on the power: `t`
* Increase voltage by 1V: `+++`
* Decrease voltage by 0.1V: `--`
* Display current status: `r`
* Quit the script: `q`


# HanmatekControl (Library version)
<a name="lib_ver"></a>
Python library to programmatically control a Hanmatek bench power supply

## Usage examples

```python
h = HanmatekControl(port)

# set 5v, 1.2a
h.set_voltage(5)
h.set_current(1.2)
h.set_power(True)

# display ratio between drawn current and maximum current
h.print_amp_meter() 
v = h.get_voltage()
```

More examples can be found inside the examples/ folder.

## Robot Framework
An example (DeviceControlTest.robot) for this library using the [Robot Framework](https://robotframework.org/) is also included. To run it, run the following command after installing [robotframework](https://pypi.org/project/robotframework/) through pip.

```bash
pip install robotframework

robot DeviceControlTest.robot
```