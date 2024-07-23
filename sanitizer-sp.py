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

    # Mangle character roll-back for indexed ports
    lines = [re.sub(r'_5', '[', line) for line in lines]
    lines = [re.sub(r'_6', ']', line) for line in lines]

    # Remove other mangle characters
    lines = [re.sub(r'_\d+', '', line) for line in lines]

    # Suffix underscore removal
    lines = [re.sub(r'_\ ', r' ', line) for line in lines]

    # Remove namespace
    lines = [re.sub(r'cell', '', line) for line in lines]

    # Add inherited supply connectors
    #lines = [re.sub(r'.ends', r'XIVDD Vdd hSup_cell\nXIVSS GND lSup_cell\n.ends', line) for line in lines]

    output_filename = filename

    with open(output_filename, 'w') as f:
        f.writelines(lines)
