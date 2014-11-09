#!/usr/bin/env python
'''Usage: d80bad <filename.d80>'''
import sys


def show_bad(input_filename):
    inp = open(input_filename, "rb")
    inp.seek(533248)

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
        if not is_valid_8050_ts(track, sector):
            sector = 0
            track += 1

        # offset of sector data in the disk image
        offset += 256

    inp.close()


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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    show_bad(sys.argv[1])
