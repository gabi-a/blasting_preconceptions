# Copyright (C) CSIRO 2012
# $Id: mod_maths.py 104 2012-07-12 06:47:38Z cha68f $

# Module of common maths functions
from math import sqrt

# Function: Calculate mean/average of a list
# Parameters: list = List of numbers
# Returns: (float, mean) average of values

def calc_mean(list):
	if len(list) < 1:
		return -1
	else:
		mean = float(0)
		for n in list:
			mean = mean + float(n)
		mean = mean / len(list)
		return mean

# Function: Calculate standard deviation of list/array
# Parameters: list = List of numbers
#             mean = Float of list values' mean
# Returns: (float, sd) standard deviation of values

def calc_sd(list, mean):
	if len(list) < 2:
		return -1
	else:
		sd = float(0)
		for n in list:
			sd = sd + (float(n) - mean)**2
		sd = sqrt(sd / (len(list)-1))
		return sd