import myio
from myhelper import str_to_int

def print_line(dev, text):
    myio.send_params([text, 0x0A], dev)

def set_font(dev, size):
    myio.send_data([0x1B, 0x21, int(size)], dev)

def set_size(dev, size):
    s = (2 << 3) * (int(size) - 1) + (int(size) - 1)
    myio.send_data([0x1D, 0x21, int(s)], dev)