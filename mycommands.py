import myio
from myhelper import str_to_int

def flush():
    myio.flush()

def print_line(text):
    myio.send_params([text, 0x0A])

def set_font(size):
    myio.send_data([0x1B, 0x21, int(size)])

def set_size(size):
    s = (2 << 3) * (int(size) - 1) + (int(size) - 1)
    myio.send_data([0x1D, 0x21, int(s)])