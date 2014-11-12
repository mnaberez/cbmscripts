#!/usr/bin/env python
'''Usage: d80bad <filename.d80>'''
import os
import sys


def print_bad(filename):
    # find the size of the disk image without the error map
    # and function to check if a t/s number is valid
    _, ext = os.path.splitext(filename)
    size, is_valid_ts = {
        '.d64': [174848, is_valid_4040_ts],
        '.d80': [533248, is_valid_8050_ts],
        '.d82': [1066496, is_valid_8250_ts]
    }[ext]

    inp = open(filename, "rb")
    inp.seek(size)

    track, sector = 1, 0
    offset = 0

    while True:
        data_byte = inp.read(1)
        if data_byte == '':
            break

        error = ord(data_byte)
        if error > 1:
            print("error %02d on %02d,%02d (offset %d / %0x hex)" % (
                error, track, sector, offset, offset))

        # increment pet track/sector counters
        sector += 1
        if not is_valid_ts(track, sector):
            sector = 0
            track += 1

        # offset of sector data in the disk image
        offset += 256

    inp.close()


def is_valid_4040_ts(track, sector):
    valid = False
    if track >= 1 and track <= 17:
        valid = sector >= 0 and sector <= 20
    elif track >= 18 and track <= 24:
        valid = sector >= 0 and sector <= 18
    elif track >= 25 and track <= 30:
        valid = sector >= 0 and sector <= 17
    elif track >= 31 and track <= 35:
        valid = sector >= 0 and sector <= 16
    return valid

def is_valid_8050_ts(track, sector):
    valid = False
    if track >= 1 and track <= 39:
        valid = sector >= 0 and sector <= 28
    elif track >= 40 and track <= 53:
        valid = sector >= 0 and sector <= 26
    elif track >= 54 and track <= 64:
        valid = sector >= 0 and sector <= 24
    elif track >= 65 and track <= 77:
        valid = sector >= 0 and sector <= 22
    return valid

def is_valid_8250_ts(track, sector):
    valid = False
    if track >= 1 and track <= 39:
        valid = sector >= 0 and sector <= 28
    elif track >= 40 and track <= 53:
        valid = sector >= 0 and sector <= 26
    elif track >= 54 and track <= 64:
        valid = sector >= 0 and sector <= 24
    elif track >= 65 and track <= 77:
        valid = sector >= 0 and sector <= 22
    elif track >= 78 and track <= 116:
        valid = sector >= 0 and sector <= 28
    elif track >= 117 and track <= 130:
        valid = sector >= 0 and sector <= 26
    elif track >= 131 and track <= 141:
        valid = sector >= 0 and sector <= 24
    elif track >= 142 and track <= 154:
        valid = sector >= 0 and sector <= 22
    return valid


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    print_bad(sys.argv[1])
