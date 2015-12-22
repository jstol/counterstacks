#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys, argparse

_BLOCK_SIZE = 4096

# Read in command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--traces', nargs='+', dest='traces', type=str, required=True)
parser.add_argument('-o', '--output', dest='output_file', type=str, required=True)
args = parser.parse_args()

files = args.traces
output_file = args.output_file

# Format the MSR files
times = {}
for name in files:
	with open(name, 'r') as original:
		for line in original:
			split = line.split(',')
			time = split[0]
			addr = int(split[4])
			size = int(split[5])
			req_type = split[3]
			if req_type == "Read":
				if time not in times:
					times[time] = []

				num_blocks = size/_BLOCK_SIZE
				
				for offset in xrange(num_blocks):
					times[time].append(addr+(offset*_BLOCK_SIZE))

# Sort and write to a new, consolidated file
sorted_times = sorted(times)
with open(output_file, 'w') as new:
	for t in sorted_times:
		addresses = times[t]
		for addr in addresses:
			new.write("{0}\n".format(addr))
