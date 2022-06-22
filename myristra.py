#!/usr/bin/python3
import os
import sys
import myio
import mycommands
import myserver

print("Myristra 0.1 fehu - Open-source ESC/POS Driver and Print Server")
print("---------------------------------------------------------------")

if __name__ == "__main__":
    #myserver.serve()
    myio.open_devices()
    myserver.serve()
    myio.close_devices()
