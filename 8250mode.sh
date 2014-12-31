#!/bin/bash
#
# Put an 8250 or SFD-1001 into double-sided (8250) or
# single-sided (8050) mode using cbmctrl.
# http://www.softwolves.com/arkiv/cbm-hackers/2/2411.html

if [ $# -lt 1 ]; then
    echo "Usage: $0 <unit number> <8050|8250>"
    exit 2
fi

if [ $# -lt 2 ] || [ $2 == 8250 ]; then
    echo "Setting unit $1 to double-sided (8250) mode"
    echo "TODO - unimplemented"
else
    echo "Setting unit $1 to single-sided (8050) mode"
    cbmctrl -p command $1 m-w 172 16 1 1
    cbmctrl -p command $1 m-w 195 16 1 0
    cbmctrl -p command $1 u9
fi
