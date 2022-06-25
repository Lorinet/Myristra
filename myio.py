import os
import sys
import bluetooth
import time
import datetime
import myconfig
import subprocess
from myhelper import delay, debug_print_hex_array

sock = None
curdev = -1

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
    if is_open() and curdev == dev:
        return
    if curdev != -1:
        close_device()
    print("Connecting to Bluetooth printers...")
    curdev = dev
    d = myconfig.devices[curdev]
    print("MAC Address: " + d)
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    serv = bluetooth.find_service(address=d)
    port = 1
    for s in serv:
        if s['host'] == d and s['protocol'] == 'RFCOMM':
            port = s['port']
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