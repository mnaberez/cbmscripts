#!/usr/bin/env python
'''Usage: d80truncate <filename.d80>'''
import sys


def trunc(filename):
    inp = open(filename, "rb")
    data = inp.read(533248)
    assert len(data) == 533248
    inp.close()

    out = open(filename, "wb")
    out.write(data)
    out.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    trunc(sys.argv[1])
