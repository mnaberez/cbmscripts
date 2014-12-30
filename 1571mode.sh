#!/bin/bash
#
# Put a 1571 into double-sided (1571) or single-sided (1541) mode
# using cbmctrl.

if [ $# -lt 1 ]; then
    echo "Usage: $0 <unit number> <1541|1571>"
    exit 2
fi

if [ $# -lt 2 ] || [ $2 == 1571 ]; then
    echo "Setting unit $1 to double-sided (1571) mode"
    cbmctrl -p command $1 u0\>m1
else
    echo "Setting unit $1 to single-sided (1541) mode"
    cbmctrl -p command $1 u0\>m0
fi
