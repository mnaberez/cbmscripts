#!/usr/bin/env python
'''Usage: d64adderror <filename.d64> <track> <sector> <error code>'''
import sys
import os

def add_errors(filename, target_track, target_sector, error_code):
    pet_track, pet_sector = 1, 0
    error_map = ''
    error_index = 0

    if os.path.getsize(filename) > 174848:
        # existing error map
        f = open(filename, "rb")
        f.seek(174848)
        error_map = list(f.read())
        f.close()
    else:
        # create a new error map
        error_map = list(chr(0) * 683)

    assert len(error_map) == 683

    # TODO: this can run forever if bad track/sector specified
    while True:
        if (pet_track == target_track) and (pet_sector == target_sector):
            error_map[error_index] = chr(error_code)
            break

        # increment error map index
        error_index += 1

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_4040_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1
    error_map = ''.join(error_map)

    f = open(filename, "rb+")
    f.seek(174848)
    f.write(error_map)
    f.close()
    assert os.path.getsize(filename) == 175531

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
    if len(sys.argv) < 5:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    add_errors(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
