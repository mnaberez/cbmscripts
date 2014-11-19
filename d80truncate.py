#!/usr/bin/env python
'''Usage: d80truncate <filename.d80>'''
import os
import sys


def trunc(filename):
    # find the size of the disk image without the error map
    _, ext = os.path.splitext(filename)
    size = {'.d64': 174848,
            '.d71': 349696,
            '.d80': 533248,
            '.d81': 819200,
            '.d82': 1066496
           }[ext]

    inp = open(filename, "rb")
    data = inp.read(size)
    assert len(data) == size
    inp.close()

    out = open(filename, "wb")
    out.write(data)
    out.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    trunc(sys.argv[1])
