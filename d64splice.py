#!/usr/bin/env python
'''Usage: d64splice <source.d64> <target.d64> <track> <sector>'''
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
        if not is_valid_4040_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # paranoia
        assert src.tell() == dest.tell()

        # stop before end of disk image since
        # an error map may follow the data
        if src.tell() == 174848:
            break

    src.close()
    dest.close()


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
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    splice(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
