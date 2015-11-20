#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""Script for generating MRCs from stack distances"""
import numpy as np
from hyperloglog.hll import HyperLogLog

class _IdealCounter(object):

	def __init__(self):
		self._set = set()

	def add_symbol(self, symbol):
		self._set.add(symbol)
	
	def process_symbol(self, symbol):
		self.add_symbol(symbol)
		return len(self._set) # return the exact number of unique elements seen

class _HLLCounter(object):

	def __init__(self, hll_error=0.01):
		self._set = HyperLogLog(hll_error)

	def add_symbol(self, symbol):
		self._set.add(symbol)
	
	def process_symbol(self, symbol):
		self.add_symbol(symbol)
		return len(self._set) # return the predicted number of unique elements seen

class CounterStack(object):

	def __init__(self, downsample_rate=10000):
		self._counters = []
		self._countmatrix = None
		self._downsample_rate = downsample_rate
		self._stack_dist_counts = {}
		self._current_step = 0

	def process_sequence_symbol(self, symbol):
		self._current_step += 1

		# Sample the counters if this is an observable time step (if it is a multiple of "d", the downsample rate)
		if self.is_observable_time():
			# Add a new counter for the current symbol
			c = _IdealCounter()
			self._counters.append(c)

			if self.is_empty():
				self._countmatrix = np.array([[c.process_symbol(symbol)]])

			else:
				# Make a new column vector containing the most recent unique count for every counter
				new_column = np.array([[counter.process_symbol(symbol)] for counter in self._counters])
				# Add the new column to the counterstack (with zeros leading up to the current counters count)
				self._countmatrix = np.append(self._countmatrix, np.zeros((1, self._countmatrix.shape[1])), axis=0)
				self._countmatrix = np.append(self._countmatrix, new_column, axis=1)

			# Update the stack distance histogram
			# delta x
			delta_x = np.diff(np.c_[np.zeros((self._countmatrix.shape[0], 1)), self._countmatrix])
			# delta y
			delta_y = np.diff(np.r_[np.zeros((1, delta_x.shape[1])), delta_x], axis=0)
			# delta_y[np.diag_indices_from(delta_y)] = self._downsample_rate - delta_x[np.diag_indices_from(delta_x)]
			delta_y[np.diag_indices_from(delta_y)] = 1 - delta_x[np.diag_indices_from(delta_x)]
			# delta_y[np.diag_indices_from(delta_y)] = 0

			delta_y_last_col = delta_y[:,-1:]
			c_last_col = self._countmatrix[:,-1:]

			for row_i in xrange(delta_y.shape[0]):
				stack_dist_count = delta_y_last_col.item(row_i, 0)
				stack_dist = c_last_col.item(row_i, 0)

				if stack_dist_count == 0:
					continue

				if not stack_dist in self._stack_dist_counts:
					self._stack_dist_counts[stack_dist] = stack_dist_count
				else:
					self._stack_dist_counts[stack_dist] += stack_dist_count
		
		# Otherwise, just update the hyperloglog streams
		else:
			for counter in self._counters:
				counter.add_symbol(symbol)

	def get_stack_distance_counts(self):
		return self._stack_dist_counts

	def is_observable_time(self):
		return self._current_step % self._downsample_rate == 0

	def is_empty(self):
		return self._countmatrix is None or len(self._countmatrix) == 0
