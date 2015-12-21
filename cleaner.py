#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys

trace_type = 'proj'

files = ["traces/{0}/{0}_0.csv", "traces/{0}/{0}_1.csv", "traces/{0}/{0}_2.csv", "traces/{0}/{0}_3.csv", "traces/{0}/{0}_4.csv"]
#files = ["traces/{0}/{0}_0.csv", "traces/{0}/{0}_1.csv"]

files = [file_name.format(trace_type) for file_name in files]

_BLOCK_SIZE = 4096

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

sorted_times = sorted(times)

with open("traces/{0}/{0}_clean.csv".format(trace_type), 'w') as new:
	for t in sorted_times:
		addresses = times[t]
		for addr in addresses:
			new.write("{0}\n".format(addr))
