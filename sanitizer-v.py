#!/usr/bin/env python3

"""
Sanitizer script to remove register and wire declarations from
fifo_synth_verilog_netlist.v and remove numbered suffixes from signals.
"""

import re
import sys

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as f:
        lines = f.readlines()

    # Remove double underscores
    lines = [re.sub(r'_{2,}', '_', line) for line in lines]

    # Mangle character removal
    lines = [re.sub(r'_[0-9]', '', line) for line in lines]

    # Remove register and wire declarations
    lines = [line for line in lines if not re.match(r'^\s*(reg|wire)\s', line)]

    # Remove cell and syn prefixes
    lines = [re.sub(r'(cell|syn)', '', line) for line in lines]

    with open(filename, 'w') as f:
        f.writelines(lines)
