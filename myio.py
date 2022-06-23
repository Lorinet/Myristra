import os
import sys
import bluetooth
import time
import datetime
import myconfig
import subprocess
from myhelper import delay, debug_print_hex_array

sock = []

def is_open():
    op = True
    for d in myconfig.devices:
        stdoutdata = subprocess.getoutput("hcitool con")
        if d not in stdoutdata.split():
            op = False
    return op

def open_devices():
    global dp
    print("Connecting to Bluetooth printers...")
    for d in myconfig.devices:
        print("MAC Address: " + d)
        sock.append(bluetooth.BluetoothSocket(bluetooth.RFCOMM))
        serv = bluetooth.find_service(address=d)
        port = 1
        for s in serv:
            if s['host'] == d and s['protocol'] == 'RFCOMM':
                port = s['port']
        print("Connecting...")
        sock[-1].connect((d, port))
        flush(len(sock) - 1)
        print("Connected")

def close_devices():
    for i in range(len(sock)):
        sock[i].close()

def send_data(dat, i):
    global dp
    print("Sending data...")
    debug_print_hex_array(dat)
    sock[i].send(bytes(dat))

def recv_byte():
    global dp
    return dp.read(1)[0]

def send_params(dat, i):
    for d in dat:
        if isinstance(d, str):
            send_data(bytes(d, "ascii"), i)
        else:
            send_data([d], i)

def flush(i):
    send_data([0x1B, 0x40], i)