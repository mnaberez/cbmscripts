#!/usr/bin/env python
'''Usage: d64diff <filename.d64> <filename.d64>'''
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
        if not is_valid_4040_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # stop before end of disk image since
        # an error map may follow the data
        if a.tell() == 174848:
            break

    a.close()
    b.close()


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


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    show_bad(sys.argv[1], sys.argv[2])
