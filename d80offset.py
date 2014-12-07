#!/usr/bin/env python
'''Usage: d80offset <filename.d80> track sector'''
import sys


def show_offset(filename, target_track, target_sector):
    pet_track, pet_sector = 1, 0
    offset = 0

    if not is_valid_8050_ts(target_track, target_sector):
        msg = "Invalid track/sector: %d/%d" % (target_track, target_sector)
        raise ValueError(msg)

    while True:
        if (pet_track == target_track) and (pet_sector == target_sector):
            print "%d,%d is offset %d (%x hex)" % (target_track, target_sector, offset, offset)
            break

        # one sector
        offset += 256

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_8050_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1


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
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    show_offset(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
