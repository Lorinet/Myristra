import myio
from myhelper import str_to_int

def flush(device, *idk):
    myio.flush(device)

def print_line(device, text):
    myio.send_params(device, [text, 0x0A])

def set_font(device, size):
    myio.send_data(device, [0x1B, 0x21, int(size)])

def set_size(device, size):
    s = (2 << 3) * (int(size) - 1) + (int(size) - 1)
    myio.send_data(device, [0x1D, 0x21, int(s)])