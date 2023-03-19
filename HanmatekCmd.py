from os import system
from sys import platform
from HanmatekControl import HanmatekControl
from cmd import Cmd
from argparse import ArgumentParser

class HanmatekCmd(Cmd):
    def __init__(self, port: str) -> None:
        super().__init__()
        self.prompt = "Hanmatek> "
        self.intro = "Hanmatek Control"
        self._port = port
        self.hc = None
        try:
            self.hc = HanmatekControl(port=self._port)
            self.prompt = f"Hanmatek ({self._port})> "
        except Exception as e:
            print("Error setting up device connection: " + str(e))
            print("You can change the serial port using the 'port' command.")
            self.prompt = "Hanmatek (disconnected)> "
    
    def do_help(self, arg: str) -> None:
        """
        help

        Display list of commands
        """
        print("Available commands (type help <topic>):")
        print("=====================================================")
        print("  help or ?         display this help text")
        print("  ports             list available serial ports")
        print("  port <portname>   change serial port")
        print("  t                 toggle power")
        print("  sv <float>        set voltage to <float>")
        print("  sc <float>        set current to <float>")
        print("  r                 read and display current status")
        print("  +[++] / -[--]     increase or decrease voltage")
        print("  q or x            exit")
        print("=====================================================")
    
    def precmd(self, line: str) -> str:
        if not len(line) == 0:
            self._lastcmd = line # intentionally not using self.lastcmd, which is used by cmd.Cmd
        else:
            line = self._lastcmd
        
        # catch +/- commands
        if 1 <= len(line) <= 4:
            sign = None
            if "+" in line:
                sign = "+"
            elif "-" in line:
                sign = "-"
            if sign is not None:
                count = line.count(sign)
                if count >= len(line)-1:
                    increment = 1 * 0.1 ** (count - 1)
                    if sign == "-":
                        increment *= -1
                    try:
                        if line[-1].isnumeric():
                            increment *= float(line[-1])
                        self.hc.set_voltage(self.hc.get_target_voltage() + increment)
                    except Exception as e:
                        print(f"Error: {e}")
                    return "pass" # required to prevent the previous command from being executed again

        # direct unit setting, e.g. 4.2V
        try:
            if line.lower().endswith("v"):
                self.do_sv(line[:-1])
                return "pass"
            elif line.lower().endswith("a"):
                self.do_sc(line[:-1])
                return "pass"
        except Exception:
            pass

        # default behaviour on every other command
        return super().precmd(line)

    def do_port(self, arg: str) -> None:
        """
        port <portname>

        Configure serial port
        """
        if self.hc is not None:
            del self.hc
        self.__init__(arg)
    
    def do_ports(self, arg: str) -> None:
        """
        ports

        List available serial ports
        """
        if 'linux' in platform.lower():
            system("ls /dev/tty*")
        else:
            system("mode")
    
    def do_t(self, args: str = "") -> None:
        """
        t

        Toggle power
        """
        if self.hc is None:
            print("Error: device not connected")
            return
        
        target_state = None
        if args.lower() in ["on", "1", "true", "yes", "enabled"]:
            target_state = True
        elif args.lower() in ["off", "0", "false", "no", "disabled"]:
            target_state = False
        
        try:
            self.hc.set_status(target_state)
        except Exception as e:
            print(f"Error: {e}")
    
    def do_sv(self, args: str):
        """
        sv <float>
        
        Set target voltage
        """
        if self.hc is None:
            print("Error: device not connected")
            return
        
        try:
            self.hc.set_voltage(float(args))
        except Exception as e:
            print(f"Error: {e}")
    
    def do_sc(self, args: str):
        """
        sc <float>

        Set target current
        """
        if self.hc is None:
            print("Error: device not connected")
            return
        
        try:
            self.hc.set_current(float(args))
        except Exception as e:
            print(f"Error: {e}")
    
    def do_r(self, unused_args: str = ""):
        """
        r

        Read and print the current device status
        """
        if self.hc is None:
            print("Error: device not connected")
            return

        self.hc.show()
    
    def do_q(self, unused_args: str = ""):
        """
        quit
        
        Quit the application
        """
        return True
    
    def do_x(self, unused_args: str = ""):
        """
        quit

        Quit the application"""
        return True

    def do_pass(self, unused_args: str = ""):
        pass

if __name__ == "__main__":
    if 'linux' in platform.lower():
        default_port = "/dev/ttyUSB0" # linux
    else:
        default_port = "COM1" # windows
    
    parser = ArgumentParser(description='Hanmatek Power Supply Control.')
    parser.add_argument('-p', '--portname', default=default_port, help='set serial port name', type=str)
    args = parser.parse_args()
    shell = HanmatekCmd(args.portname)
    shell.cmdloop()