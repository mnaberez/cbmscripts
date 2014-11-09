#!/usr/bin/env python
'''Usage: d80splice <source.d80> <target.d80> <track> <sector>'''
import sys
import os

def splice(src_filename, dest_filename, splice_track, splice_sector):
    src = open(src_filename, "rb")
    src.seek(0)
    dest = open(dest_filename, "rb+")
    dest.seek(0)

    pet_track, pet_sector = 1, 0

    while True:
        src_sector = src.read(256)
        assert len(src_sector) == 256

        if (pet_track == splice_track) and (pet_sector == splice_sector):
            print "spliced %d,%d into %s" % (splice_track, splice_sector, dest_filename)
            dest.write(src_sector)
        else:
            dest.seek(256, os.SEEK_CUR)

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_8050_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # paranoia
        assert src.tell() == dest.tell()

        # stop before end of disk image since
        # an error map may follow the data
        if src.tell() == 533248:
            break

    src.close()
    dest.close()


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

    splice(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
