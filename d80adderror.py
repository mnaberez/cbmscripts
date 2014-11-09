#!/usr/bin/env python
'''Usage: d80adderror <filename.d80> <track> <sector> <error code>'''
import sys
import os

def add_errors(filename, target_track, target_sector, error_code):
    pet_track, pet_sector = 1, 0
    error_map = ''
    error_index = 0

    if os.path.getsize(filename) > 533248:
        # existing error map
        f = open(filename, "rb")
        f.seek(533248)
        error_map = list(f.read())
        f.close()
    else:
        # create a new error map
        error_map = list(chr(0) * 2083)

    assert len(error_map) == 2083

    # TODO: this can run forever if bad track/sector specified
    while True:
        if (pet_track == target_track) and (pet_sector == target_sector):
            error_map[error_index] = chr(error_code)
            break

        # increment error map index
        error_index += 1

        # increment pet track/sector counters
        pet_sector += 1
        if not is_valid_8050_ts(pet_track, pet_sector):
            pet_sector = 0
            pet_track += 1
    error_map = ''.join(error_map)

    f = open(filename, "rb+")
    f.seek(533248)
    f.write(error_map)
    f.close()
    assert os.path.getsize(filename) == 535331

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
    if len(sys.argv) < 5:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    add_errors(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
