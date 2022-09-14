import os
from re import S
import sys
import socket
import time
import datetime
import myconfig
import subprocess
from myhelper import delay, debug_print_hex_array

sock = None
curdev = -1
port = 1

def is_open():
    global curdev
    global sock
    if curdev == -1:
        return False
    stdoutdata = subprocess.getoutput("hcitool con")
    if myconfig.devices[curdev] not in stdoutdata.split():
        return False
    return True

def open_device(dev):
    global curdev
    global sock
    global port
    if is_open() and curdev == dev:
        return
    if curdev != -1:
        close_device()
    print("Connecting to Bluetooth printers...")
    curdev = dev
    d = myconfig.devices[curdev]
    print("MAC Address: " + d)
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    print("Connecting...")
    sock.connect((d, port))
    flush()
    print("Connected")

def close_device():
    sock.close()

def send_data(dat):
    global dp
    print("Sending data...")
    debug_print_hex_array(dat)
    sock.send(bytes(dat))
    time.sleep(0.1)

def recv_byte():
    global dp
    return dp.read(1)[0]

def send_params(dat):
    for d in dat:
        if isinstance(d, str):
            send_data(bytes(d, "ascii"))
        else:
            send_data([d])

def flush():
    send_data([0x1B, 0x40])