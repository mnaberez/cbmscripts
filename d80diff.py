#!/usr/bin/env python
'''Usage: d80diff <filename.d80> <filename.d80>'''
import sys


def show_bad(a_filename, b_filename):
    a = open(a_filename, "rb")
    b = open(b_filename, "rb")

    pet_track, pet_sector = 1, 0

    while True:
        a_sector = a.read(256)
        b_sector = b.read(256)

        if (a_sector == '') or (b_sector == ''):
            break # no data

        if a_sector != b_sector:
            print "%02d,%02d differ" % (pet_track, pet_sector)

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_8050_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # stop before end of disk image since
        # an error map may follow the data
        if a.tell() == 533248:
            break

    a.close()
    b.close()


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
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    show_bad(sys.argv[1], sys.argv[2])
