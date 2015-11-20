#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function, unicode_literals
with open('traces/web/web_0.csv', 'r') as original:
	with open('traces/web/web_0_clean.csv', 'w') as new:
		for line in original:
			split = line.split(',')
			if split[3] == "Read":
				new.write("{0}\n".format(split[4]))
