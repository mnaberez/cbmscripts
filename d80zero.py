#!/usr/bin/env python
'''Usage: d80diff <filename.d80> <filename.d80>'''
import sys
import os

def zero(filename, target_track, target_sector):
    f = open(filename, "rb+")
    f.seek(0)

    pet_track, pet_sector = 1, 0

    while True:
        if (pet_track == target_track) and (pet_sector == target_sector):
            print "zeroed %d,%d of %s" % (target_track, target_sector, filename)
            f.write(chr(0) * 256)
        else:
            f.seek(256, os.SEEK_CUR)

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_8050_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # stop before end of disk image since
        # an error map may follow the data
        if f.tell() == 533248:
            break

    f.close()


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

    zero(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
