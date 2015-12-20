#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""Script for generating MRCs from stack distances"""
import numpy as np
from hyperloglog.shll import SlidingHyperLogLog
import sys

class CounterStack(object):
	"""Class that takes a stream of input symbols and keeps track of stack distances"""
	def __init__(self, downsample_rate=10000):
		self._lastcounts = None
		self._downsample_rate = downsample_rate
		self._stack_dist_counts = {}
		self._current_step = None
		self._shll = SlidingHyperLogLog(0.3, float("inf"))
		self._countmatrix = []

	def process_sequence_symbol(self, symbol):
		# Current step starts at 0
		self._current_step = 0 if self._current_step is None else self._current_step+1
		# Symbol count starts at 1
		self._symbol_count = self._current_step + 1

		# Add the current symbol to the sliding HLL counter
		self._shll.add(self._current_step, symbol)

		# Sample the counters if this is an observable time step (if it is a multiple of "d", the downsample rate)
		if self.is_observable_time():
			if self.is_empty():
				self._lastcounts = np.zeros((1, 1))

			else:
				# Make a new column vector containing the most recent unique count for every counter
				self._lastcounts = np.vstack((self._lastcounts, np.zeros((1, 1))))

			# Get list of unique counts, given an interval (xrange) of windows. Stack as col vector
			new_counts = self._shll.card_wlist(self._symbol_count, xrange(1, self._current_step+self._downsample_rate, self._downsample_rate))
			new_counts_column = np.array(new_counts)[::-1].reshape(-1,1)

			# Make a matrix containing only the last two rows
			countmatrix = np.c_[self._lastcounts, new_counts_column]
			self._countmatrix = countmatrix

			# Update the stack distance histogram
			# Compute differences between the last two columns
			delta_x = np.diff(countmatrix)

			# Compute change between the change in the counters (delta Y)
			delta_y = np.diff(np.r_[np.zeros((1, delta_x.shape[1])), delta_x], axis=0)
			
			# Set the last element in delta y to 1-delta_x (according to the algorithm)
			delta_y[-1,-1] = 1 - delta_x[-1,-1]
			delta_y_last_col = delta_y[:,-1:] # Not sure if this is needed anymore since delta_y is probably just 1 col now, but just to be safe
			c_last_col = countmatrix[:,-1:]

			# Go across all rows
			for row_i in xrange(delta_y.shape[0]):
				# Get the stack distance count from delta y
				stack_dist_count = delta_y_last_col.item(row_i, 0)
				# Get the stack distance from the counterstacks "matrix" (only need last two col of it)
				stack_dist = c_last_col.item(row_i, 0)

				# Only record stack distances that don't have a count of 0 (to save memory)
				if stack_dist_count == 0:
					continue

				# We record the stack distance/the downsample rate, 'd' (according to the algorithm)
				if np.ceil(stack_dist/float(self._downsample_rate)) not in self._stack_dist_counts:
					self._stack_dist_counts[np.ceil(stack_dist/float(self._downsample_rate))] = stack_dist_count
				else:
					self._stack_dist_counts[np.ceil(stack_dist/float(self._downsample_rate))] += stack_dist_count
		
			# Record the newest column of counter values for the next round
			self._lastcounts = new_counts_column

	def get_stack_distance_counts(self):
		# Sort bin/value pairs by bin number
		# Multiply bins by delta (downsample rate) according to algorithm
		bins, values = map(list, zip(*sorted(self._stack_dist_counts.items(), key=lambda t: t[0])))
		bins = [x*self._downsample_rate for x in bins]
		return bins, values

	def is_observable_time(self):
		return self._current_step % self._downsample_rate == 0

	def is_empty(self):
		return self._lastcounts is None or len(self._lastcounts) == 0

	def total_size(self):
		return(sys.getsizeof(self._countmatrix))
