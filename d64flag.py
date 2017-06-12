#!/usr/bin/env python
'''Detect if disk is single sided (1541) or double sided (1571)
Usage: d64flag <filename.d64>'''
import sys


def show_double_sided_flag(filename):
    with open(filename, "rb") as a:
        pet_track, pet_sector = 1, 0
        while True:
            sector_data = a.read(256)
            if (sector_data == ''):
                break # no data

            if (pet_track == 18) and (pet_sector == 0):
                value = ord(sector_data[3])
                sys.stdout.write("  Track 18, Sector 0, Offset 3 = 0x%02x " %
                                 value)
                if (value & 0x80) > 0:
                    sys.stdout.write("(indicates double sided: 1571)\n")
                else:
                    sys.stdout.write("(indicates single sided: 1541)\n")
                break

            # increment pet track/sector counters
            pet_sector += 1
            if not is_valid_1571_ts(pet_track, pet_sector):
                pet_sector = 0
                pet_track += 1

def show_1571_ts_pointers(filename):
    with open(filename, "rb") as a:
        pet_track, pet_sector = 1, 0
        while True:
            sector_data = a.read(256)
            if (sector_data == ''):
                break # no data

            t, s = [ ord(x) for x in sector_data[0:2] ]
            if (t > 35) and (t < 71):
                sys.stdout.write(
                    "  Track %d, Sector %d: Sector points to 1571 T%d/S%d\n" % (
                    pet_track, pet_sector, t, s))

            # increment pet track/sector counters
            pet_sector += 1
            if not is_valid_1571_ts(pet_track, pet_sector):
                pet_sector = 0
                pet_track += 1


def is_valid_1571_ts(track, sector):
    valid = False
    if track >= 1 and track <= 17:
        valid = sector >= 0 and sector <= 20
    elif track >= 18 and track <= 24:
        valid = sector >= 0 and sector <= 18
    elif track >= 25 and track <= 30:
        valid = sector >= 0 and sector <= 17
    elif track >= 31 and track <= 35:
        valid = sector >= 0 and sector <= 16
    elif track >= 36 and track <= 52:
        valid = sector >= 0 and sector <= 20
    elif track >= 53 and track <= 59:
        valid = sector >= 0 and sector <= 18
    elif track >= 60 and track <= 65:
        valid = sector >= 0 and sector <= 17
    elif track >= 66 and track <= 70:
        valid = sector >= 0 and sector <= 16
    return valid


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    sys.stdout.write("\n%s\n" % sys.argv[1])
    show_double_sided_flag(sys.argv[1])
    show_1571_ts_pointers(sys.argv[1])
