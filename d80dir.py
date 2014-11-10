#!/usr/bin/env python
'''Usage: d80dir <filename.d80>'''
import os
import subprocess
import sys
import tempfile

def print_dir(filename):
    # find the size of the disk image without the error map
    _, ext = os.path.splitext(filename)
    size = {'.d64': 174848, '.d80': 533248}[ext]

    # if the image has error info at the end, c1541 can't read it,
    # so create a tempfile without the error info
    tmpfile = None
    if os.path.getsize(filename) > size:
        tmpfile = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        with open(filename, 'rb') as f:
            data = f.read(size)
            tmpfile.write(data)
            tmpfile.close()
            filename = tmpfile.name

    # scrape output from c1541
    proc = subprocess.Popen("c1541 '%s'" % filename, shell=True,
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    lines = proc.communicate("dir\n")[0].split("\n")

    # remove leading version/copyright info
    for i, line in enumerate(lines):
        if line.startswith("c1541 #8>"):
            break
    lines = lines[i:]

    # remove prompts and empty lines
    lines = [ l.replace('c1541 #8> ', '') for l in lines ]
    lines = [ l for l in lines if len(l.strip()) > 0 ]

    # print the directory
    for line in lines:
        print(line)

    # unlink tempfile if we made one
    if tmpfile:
        os.unlink(tmpfile.name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)

    print_dir(sys.argv[1])
