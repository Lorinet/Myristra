import time

def delay(sex: float):
    time.sleep(sex / 1000)

def debug_print_hex_array(arrn):
    strg = "["
    for x in arrn:
        strg += hex(x)[2:] + " "
    strg = strg[:len(strg) - 1]
    strg += "]"
    print(strg)

def str_to_int(s):
    return bytes(int(s))