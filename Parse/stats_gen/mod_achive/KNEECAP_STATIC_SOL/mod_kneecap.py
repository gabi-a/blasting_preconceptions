# Copyright (C) CSIRO 2012
# $Id: mod_kneecap.py 116 2012-08-31 05:11:33Z cha68f $

# Module of common XML functions
from itertools import groupby

# Function: Groups the values of a list together based on value and 
#           returns a list of the values which contain over the parameter
#           percentile of total occurences
# Parameters: list = List of numeric values
#             xcount = Number of coordinate pairs wanted on histogram
# Returns: (float, maxx) maximum x axis value,
#          (float, maxy) maximum y axis value,
#          (list, capped_list) list of values and the respective total occurences

def cap_list(values,cap_percentage):
	if len(values) < 2:
		return values[0],1,[(values[0],1)]
	else:
		capped_list = []
		maxx = 0
		cap_value = cap_percentage * len(values)
		
		group_list = [(a,len(list(b))) for a,b in groupby(sorted(values))]
		
		for n in group_list:
			if n[1] >= cap_value:
				capped_list.append(n)
				if n[0] > maxx:
					maxx = n[0]
		
		maxy = len(capped_list)
		
		return maxx,maxy,capped_list