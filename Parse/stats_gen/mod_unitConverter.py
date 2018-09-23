# Copyright (C) CSIRO 2012
# $Id: mod_unitConverter.py 132 2012-12-20 08:11:29Z cha68f $

# Module of conversions between scientific units

# Lists of valid units acceptable for conversion,
# these are grouped by W/V (weight/volume),
# V/V (volume/volume), M (molar) and MISC (others)

VALID_UNITS_MISC=["%"]
VALID_UNITS_WV=["W/V","G/ML","MG/ML","UG/ML"]
VALID_UNITS_M=["M","MM","UM"]
VALID_UNITS_VV=["V/V","MV/V"]

# Main units acceptable to be converted to

STANDARD_UNITS=["W/V","M","V/V"]

TYPE_WV=1
TYPE_M=2
TYPE_VV=3

NOT_AVAILABLE=-999

# Function: Finds which group of units current unit belongs to
# Parameters: unit_str = String of current source unit
#             dens_exist = Density value of source chemical
# Returns: (int) Units group type ID

def get_unit_type(unit_str,dens_exist):
	unit_str = unit_str.upper()
	if unit_str in VALID_UNITS_VV:
		return TYPE_VV
	if unit_str in VALID_UNITS_M:
		return TYPE_M
	if unit_str in VALID_UNITS_WV:
		return TYPE_WV
	if unit_str in VALID_UNITS_MISC:
		if dens_exist > -2:
			return TYPE_VV
		else:
			return TYPE_WV
	return NOT_AVAILABLE


def dynamic_convert_to_unit_type(from_unit_str,to_unit_str,unit_num,dens_exist,mw_exist):
	from_unit_str = from_unit_str.upper()
	to_unit_str = to_unit_str.upper()
	
	to_unit = get_unit_type(to_unit_str,dens_exist)
	
	if to_unit == TYPE_WV:
		return convert_unit_to_wv(from_unit_str,unit_num,dens_exist,mw_exist)
	if to_unit == TYPE_M:
		return convert_unit_to_M(from_unit_str,unit_num,dens_exist,mw_exist)
	if to_unit == TYPE_VV:
		convert_unit_to_vv(from_unit_str,unit_num,dens_exist,mw_exist)
	
	return NOT_AVAILABLE


# Parameters: unit_str/unit_str_input = String of current source unit
#             unit_num = Value to be converted
#             density = Density value of source chemical
#             mw = Molecular weight of source chemical
# Returns: (float) converted value


# Functions to convert units to W/V

def convert_wv_to_wv(unit_str,unit_num):
	unit_str = unit_str.upper()
	if unit_str == "%":
		return unit_num
	else:
		if unit_str in STANDARD_UNITS:
			return unit_num
		else:
			new_num = unit_num*100
			if unit_str == "G/ML":
				return new_num
			if unit_str == "MG/ML":
				return new_num/1000
			if unit_str == "UG/ML":
				return new_num/1000000
	return NOT_AVAILABLE

def convert_M_to_wv(unit_str,unit_num,mw):
	unit_str = unit_str.upper()
	if unit_str == "M":
		return (unit_num*mw)/10
	if unit_str == "MM":
		return ((unit_num/1000)*mw)/10
	if unit_str == "UM":
		return ((unit_num/1000000)*mw)/10
	return NOT_AVAILABLE

def convert_vv_to_wv(unit_str,unit_num,density):
	unit_str = unit_str.upper()
	if unit_str == "V/V":
		return unit_num/density
	if unit_str == "%":
		return unit_num/density
	return NOT_AVAILABLE

def convert_unit_to_wv(unit_str_input,unit_num,density,mw):
	unit_str = unit_str_input.upper()
	unit_num = float(unit_num)
	density = float(density)
	mw = float(mw)
	type = get_unit_type(unit_str,density)
	if type == TYPE_WV:
		unit_wv = convert_wv_to_wv(unit_str,unit_num)
	if type == TYPE_M:
		unit_wv = convert_M_to_wv(unit_str,unit_num,mw)
	if type == TYPE_VV:
		unit_wv = convert_vv_to_wv(unit_str,unit_num,density)
	return unit_wv

# Functions to convert units to M

def convert_wv_to_M(unit_str,unit_num,mw):
	unit_str = unit_str.upper()
	if unit_str == "%":
		return (unit_num*10)/mw
	if unit_str == "W/V":
		return (unit_num*10)/mw
	if unit_str == "G/ML":
		return unit_num/mw
	if unit_str == "MG/ML":
		return (unit_num*1000)/mw
	if unit_str == "UG/ML":
		return (unit_num*1000000)/mw
	return -NOT_AVAILABLE

def convert_M_to_M(unit_str,unit_num):
	unit_str = unit_str.upper()
	if unit_str in STANDARD_UNITS:
		return unit_num
	if unit_str == "MM":
		return unit_num/1000
	if unit_str == "UM":
		return unit_num/1000000
	return NOT_AVAILABLE

def convert_vv_to_M(unit_str,unit_num,density,mw):
	unit_str = unit_str.upper()
	if unit_str == "V/V":
		return (unit_num*density*10)/mw
	if unit_str == "%":
		return (unit_num*density*10)/mw
	return NOT_AVAILABLE

def convert_unit_to_M(unit_str_input,unit_num,density,mw):
	unit_str = unit_str_input.upper()
	unit_num = float(unit_num)
	density = float(density)
	mw = float(mw)
	type = get_unit_type(unit_str,density)
	if type == TYPE_WV:
		unit_M = convert_wv_to_M(unit_str,unit_num,mw)
	if type == TYPE_M:
		unit_M = convert_M_to_M(unit_str,unit_num)
	if type == TYPE_VV:
		unit_M = convert_vv_to_M(unit_str,unit_num,density,mw)
	return unit_M
	
# Functions to convert units to V/V

def convert_vv_to_vv(unit_str,unit_num):
	unit_str = unit_str.upper()
	if unit_str == "%":
		return unit_num
	else:
		if unit_str in STANDARD_UNITS:
			return unit_num
		else:
			if unit_str == "MV/V":
				return unit_num/1000
	return NOT_AVAILABLE

def convert_wv_to_vv(unit_str,unit_num,density):
	unit_str = unit_str.upper()
	if unit_str == "W/V":
		return unit_num*density
	if unit_str == "%":
		return unit_num*density
	return NOT_AVAILABLE

def convert_M_to_vv(unit_str,unit_num,mw,density):
	unit_str = unit_str.upper()
	unit_wv = convert_M_to_wv(unit_str,unit_num,mw)
	unit_vv = convert_wv_to_vv("W/V",unit_wv,density)
	return unit_vv

def convert_unit_to_vv(unit_str_input,unit_num,density,mw):
	unit_str = unit_str_input.upper()
	unit_num = float(unit_num)
	density = float(density)
	mw = float(mw)
	type = get_unit_type(unit_str,density)
	if type == TYPE_WV:
		unit_vv = convert_wv_to_vv(unit_str,unit_num,density)
	if type == TYPE_M:
		unit_vv = convert_M_to_vv(unit_str,unit_num,mw,density)
	if type == TYPE_VV:
		unit_vv = convert_vv_to_vv(unit_str,unit_num)
	return unit_vv