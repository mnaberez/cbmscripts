#!/usr/bin/env python
'''Usage: d80splice <source.d80> <target.d80> <track> <sector>'''
import sys
import os

def splice(src_filename, dest_filename, splice_track, splice_sector):
    # both images must be the same type
    _, src_ext = os.path.splitext(src_filename)
    _, dest_ext = os.path.splitext(dest_filename)
    assert src_ext == dest_ext

    # find the size of the disk image without the error map
    # and function to check if a t/s number is valid
    size, is_valid_ts = {
        '.d64': [174848, is_valid_1541_ts],
        '.d71': [349696, is_valid_1571_ts],
        '.d80': [533248, is_valid_8050_ts],
        '.d81': [819200, is_valid_1581_ts],
        '.d82': [1066496, is_valid_8250_ts]
    }[src_ext]

    if not is_valid_ts(splice_track, splice_sector):
        msg = "Invalid track/sector: %d/%d" % (splice_track, splice_sector)
        raise ValueError(msg)

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
        if not is_valid_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1

        # paranoia
        assert src.tell() == dest.tell()

        # stop before end of disk image since
        # an error map may follow the data
        if src.tell() == size:
            break

    src.close()
    dest.close()


def is_valid_1541_ts(track, sector):
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

def is_valid_1581_ts(track, sector):
    valid = False
    if track >= 1 and track <= 80:
        valid = sector >= 0 and sector <= 39
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
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    splice(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
