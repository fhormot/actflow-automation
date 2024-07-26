#!/usr/bin/env python3

"""
Verilog export & sanitization using interact
"""

import subprocess
import argparse
import re
import os

script_interact_name = 'script-interact'

def prepare_interact(process, input_file, output_file):
    """
    Prepare input file
    """
    script = [f'act:read {input_file}',
        f'act:localize Reset',
        f'act:expand',
        f'act:top {process}',
        f'ckt:cell-map',
        f'ckt:cell-save {output_file.split('.')[0]}-gates.act',
        f'conf:set_int "act2v.name_mangle" 1',
        f'ckt:save-vnet -nocell {output_file}']

    with open(script_interact_name, 'w') as f:
        for command in script:
            f.write(f'{command}\n')

    os.chmod(script_interact_name, 0o777)

def execute_interact(tech_name):
    """
    Execute script "prs2net"
    """

    tech_arg = f'-T{tech_name}' if tech_name else ""

    cmd = f"interact -ref=1 {tech_arg} < {script_interact_name}"
    subprocess.call(cmd, shell=True)

def export_gates(input_file, output_file, tech_name):
    """
    Execute bulk export script for prs2net
    """

    tech_arg = f'-T {tech_name}' if tech_name else ""

    cmd = f"script-prs2net.py {tech_arg} -i {output_file.split('.')[0]}-gates.act -o {output_file.split('.')[0]}-gates.sp"
    subprocess.call(cmd, shell=True)

def sanitize_interact(output_file):
    """
    Execute script "sanitizer-v"
    """
    cmd = f"sanitizer-v.py {output_file}"
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file containing prs process.")
    parser.add_argument("-p", "--process", help="process name.")
    parser.add_argument("-o", "--output", help="Output Verilog netlist file.")
    parser.add_argument("-T", "--tech", help="Technology select.")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    process_name = args.process
    tech_name = args.tech if args.tech else ""

    prepare_interact(process_name, input_file, output_file)
    execute_interact(tech_name)
    sanitize_interact(output_file)

    # Cleanup the script file
    os.remove(script_interact_name)

    #Export gates to SPICE
    export_gates(input_file, output_file, tech_name)
