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
command_buffers = {}

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
    flush(dev)
    print("Connected")

def close_device():
    sock.close()

def send_data(dev, dat):
    global command_buffers;
    print("Sending data...")
    debug_print_hex_array(dat)
    if not dev in command_buffers.keys():
        command_buffers[dev] = []
    command_buffers[dev] += dat;

def send_params(dev, dat):
    for d in dat:
        if isinstance(d, str):
            send_data(dev, bytes(d, "ascii"))
        else:
            send_data(dev, [d])

def flush(dev):
    global sock;
    global command_buffers;
    if dev not in command_buffers.keys():
        command_buffers[dev] = []
        print("added")
    command_buffers[dev] += [0x1B, 0x40];
    open_device(int(dev))
    if dev not in command_buffers.keys():
        return
    sock.send(bytes(command_buffers[dev]))
    del command_buffers[dev];
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()