# Copyright (C) CSIRO 2012
# $Id: mod_dynamicKneecap.py 133 2012-12-20 08:49:16Z cha68f $

# Module of common XML functions
from itertools import groupby

FILTER_COUNT = 2
AVERANGE_RANGE = 8		# the total count of values on either side
NOT_AVAILABLE = -999
NOT_SET = -2
TRUE = 0
FALSE = 1

# Function: Calculates current average of lists of values to the left and right
# Parameters: left_v = List of values to the left and including current value
#             right_v = List of values to the right of current value
# Returns: (float, average)

def calc_current_average(left_v, right_v):
	average = float(0.0)
	count = len(left_v) + len(right_v)
	
	#print "COUNT   ",
	#print count,
	
	if count > 0:
		if len(left_v) > 0:
			for n in left_v:
				average += n[1]
		#print "   LEFT   ",
		#print average,
		if len(right_v) > 0:
			for n in right_v:
				average += n[1]
		#print "   RIGHT   ",
		#print average
		average = average/float(count)
	
	return average

# Function: Creates sliding window function to slide through all values
#           in list, and removes values which are lower than the current
#           average of the values in the sliding window
# Parameters: group_list = List of numeric values
# Returns: (float, maxy) maximum y axis value,
#          (list, capped_list) list of values and the respective total occurences

def filter_list(group_list):
	if len(group_list) < 2:
		return group_list[0][1],[group_list[0]]
	else:
		capped_list = []
		maxy = 0
		ave_lists_count = AVERANGE_RANGE
		
		if AVERANGE_RANGE/2 > len(group_list):
			ave_lists_count = len(group_list)/2
		
		#print group_list
		
		if len(group_list) < 2:
			return group_list[0][0],len(group_list),[group_list[0]]
		
		left_values = []
		right_values = group_list[0:(ave_lists_count+1)]
		curr_ave = float(0.0)
		curr_index = 0
		
		for n in group_list:
			
			if curr_index >= ave_lists_count:
				if len(left_values) >= ave_lists_count:
					left_values.pop(0)
				
				left_values.append(right_values.pop(0))
				
				if right_values >= ave_lists_count:
					if curr_index <= (len(group_list)-ave_lists_count):
						if (curr_index+ave_lists_count) < len(group_list):
							#print group_list[curr_index+ave_lists_count]
							right_values.append(group_list[curr_index+ave_lists_count])
			
			#print "LEFT ARRAY   ",
			#print left_values
			#print "RIGHT ARRAY   ",
			#print right_values
			
			curr_ave = calc_current_average(left_values,right_values)
			
			#print "CURR AVE   ",
			#print curr_ave
			
			if n[1] >= curr_ave:
				capped_list.append(n)
				if n[1] > maxy:
					maxy = n[1]
			
			curr_index+=1
		
		return maxy,capped_list

# Function: Groups the values of a list together based on value and 
#           returns a list of the values which contain over the parameter
#           percentile of total occurences
# Parameters: list = List of numeric values
#             xcount = Number of coordinate pairs wanted on histogram
# Returns: (float, maxx) maximum x axis value,
#          (float, maxy) maximum y axis value,
#          (list, capped_list) list of values and the respective total occurences

def get_capped_list(values):
	if len(values) < 2:
		return values[0],len(values),[(values[0],1)]
	else:
		#print "START CHEM"
		group_list = []
		capped_list = []
		cap_count = 0
		maxy = 0
		
		group_list = [(a,len(list(b))) for a,b in groupby(sorted(values))]
		
		while (cap_count < FILTER_COUNT):
			maxy,capped_list = filter_list(group_list)
			cap_count+=1
			group_list[:] = []
			group_list = capped_list
		
		maxx = len(capped_list)
		
		#print values
		#print capped_list
		#exit()
		
		#print "FINISHED CURRENT CHEM"
		
		return maxx,maxy,capped_list