#!/usr/bin/env python3

"""
Bulk export & sanitization of prs2net
"""

import subprocess
import argparse
import re
import os

def execute_prs2net(item, filename, tech_name):
    """
    Execute script "prs2net"
    """

    tech_arg = f'-T{tech_name}' if tech_name else ""

    cmd = f"prs2net {tech_arg} -p cell::{item} -o {item}.sp {filename}"
    print(f'{cmd}')
    subprocess.call(cmd, shell=True)

def execute_sanitizer(item):
    """
    Execute script "sanitizer"
    """
    cmd = f"sanitizer-sp.py {item}.sp"
    subprocess.call(cmd, shell=True)

def retrieve_processes(filename):
    with open(filename) as f:
        list_proc = f.read().splitlines()

    # Get all defining lines (e.g. export defcell ginvc0)
    list_proc = [line for line in list_proc if 'defcell' in line]

    # Remove any templated defcells
    list_proc = [line for line in list_proc if not 'template' in line]

    # Remove text before process name
    list_proc = [re.sub(r'export defcell ', r'', line) for line in list_proc]

    # Remove portlist
    list_proc = [re.sub(r' \(.*\)', r'', line) for line in list_proc]

    # Any usable names will be a single word at this point
    list_proc = [line for line in list_proc if not len(line.split())-1]

    return list_proc

def join_files(input_files, output_file):
    with open(output_file, 'w') as outfile:
        process_list = []

        for filename in input_files:
            with open(f'{filename}.sp') as infile:
                for line in infile:
                    if line.startswith('.subckt'):
                        process_list.append(line.split(' ')[1])

                    outfile.write(line)
                    
            # Delete the input file
            os.remove(f'{filename}.sp')

        outfile.seek(0,0)
        outfile.write(f'* List of processes: ' + ' '.join(process_list) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file containing prs declarations.")
    parser.add_argument("-o", "--output", help="Output SPICE file.")
    parser.add_argument("-T", "--tech", help="Technology select.")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    tech_name = args.tech if args.tech else ""

    # Get list of processes from file
    list_proc = retrieve_processes(input_file)

    for item in list_proc:
      execute_prs2net(item, input_file, tech_name)
      execute_sanitizer(item)

    join_files(list_proc, output_file)

