#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""Script for generating MRCs from stack distances"""
import matplotlib.pyplot as plt
import numpy as np
import pprint

from cs import CounterStack

def generate_mrc(trace_filename):
	# Read in file
	counterstack = CounterStack(1000)
	#counterstack = CounterStack(30)
	steps = 1
	with open(trace_filename, 'r') as f:
		for line in f:
			symbol = line.rstrip()
			counterstack.process_sequence_symbol(symbol)

			print(steps)
			steps+=1

	bins, values = counterstack.get_stack_distance_counts()

	# Print all the counts
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(zip(bins, values))
	# Print the total cumulative sum of all counts
	print(np.sum(values))

	# Carry any fully negative buckets over
	# neg = 0
	# total = 0
	# vals = []
	# for i in xrange(len(stack_dist_counts)):
	# 	val = stack_dist_counts.values()[i]
	# 	if neg < 0:
	# 		val += neg

	# 	if val < 0:
	# 		neg = val
	# 	else:
	# 		neg = 0
	# 		total += val

	# 	vals.append(total/float(steps))

	# vals = np.cumsum(stack_dist_counts.values())/float(steps)
	vals = np.cumsum(values)

	plt.plot(bins, vals)
	# plt.hist(vals, bins=bins, histtype='step', cumulative=True)# , bins=stack_dist_counts.keys()) # plt.hist#, histtype='step')#, weights=np.zeros_like(stack_dist_counts.values()) + 1./(np.sum(np.array(stack_dist_counts.values()))))
	plt.title("Hit Ratio Chart")
	plt.xlabel("Cache Size (number of blocks)")
	plt.ylabel("Hit Ratio")
	plt.show()

	raw_input('Press enter to continue...')

if __name__ == '__main__':
	generate_mrc('traces/web/web_0_clean.csv')
	#generate_mrc('traces/normal_137979.trace')

