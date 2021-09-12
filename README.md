# hanmatek-cmd (cli version)
Quick and dirty Python implementation to interactively control a Hanmatek Bench Power Supply

For a [library version](#lib_ver_), see below.

## Background
The power supply sits behind my monitor, therefore I cannot easily access the built in interface. Hence I created this little and very simple python script that implements the most basic functionality I use on a day to day basis.  
It uses the minimalmodbus library to read and write data over the power supplies USB interface.

## Installation
Install the minimalmodbus library by running `pip -r requirements.txt`.
On Linux you may also need to grant permission to your user to use the serial interface (/dev/ttyUSB0 in my case).

## Usage
First, make sure the serial port defined at the beginning of the script is correct. Then just run the script.

```
command reference:
  h or ?         display this help text
  t              toggle power
  sv <float>     set voltage to <float>
  sc <float>     set current to <float>
  r              read current power supply configuration
  +[++] / -[--]  increase or decrease voltage
  q or x         exit
```

If no new input is provided and the enter button is pressed, the previous command will be repeated. This makes it easy to step the voltage up or down continuously.

### Some examples in reasonable order

* Running the script: `python hanmatek-cmd.py`
* Setting voltage to 3.3V: `sv 3.3`
* Setting current limiter to 0.2A: `sc 0.2`
* Turn on the power: `t`
* Increase voltage by 1V: `+++`
* Decrease voltage by 0.1V: `--`
* Display current configuration: `r`
* Quit the script: `q`


# HanmatekControl (Library version)
<a name="lib_ver"></a>
Quick and dirty Python implementation to programmatically control a Hanmatek Bench Power Supply

## Usage example
An example for using the [Robot Framework](https://robotframework.org/) with this library is also included

```python
h = HanmatekControl(port)
h.set_voltage(5)
h.set_power(True)
h.set_current(0.5)
```