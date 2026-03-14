from HanmatekCmd import HanmatekCmd

def main():
    shell = HanmatekCmd("COM5")
    shell.cmdloop()

if __name__ == "__main__":
    main()
