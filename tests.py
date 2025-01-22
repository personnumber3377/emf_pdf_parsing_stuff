#!/bin/python3

from generate import *
import os
import importlib # This is to load the changes of the test spec file...
from util import *

TEST_SPEC_FILENAME = "test_spec.py"
TEST_SPEC_MODULE_NAME = "test_spec"

cur_module = None # This is the current test spec module. This will be loaded in write_to_test_spec_and_import

DEBUG = True

def dprint(string): # Debug print here...
	if DEBUG:
		print("[DEBUG] "+str(string))
	return

def good(string):
	if DEBUG:
		print("[+] "+str(string))
	return


def write_to_test_spec_and_import(contents): # This writes the data to a file called test_spec.py which is then imported in the tests and then the contents are checked for something in the test functions. After this the data is imported into this python file.
	global cur_module
	print("contents == "+str(contents))
	os.system("rm "+str(TEST_SPEC_FILENAME)) # Remove the old file...
	fh = open(TEST_SPEC_FILENAME, "w")
	fh.write(contents)
	fh.close()
	cur_module = importlib.import_module(TEST_SPEC_MODULE_NAME) # Try to load the thing...
	dprint("Here are the contents of the module: "+str(dir(cur_module)))
	return

'''
3.2.22 EMR_EOF Example
This section provides an example of an EMR_EOF record (section 2.3.4.1).
000037E0: 0E 00 00 00 14 00 00 00
000037F0:00 00 00 00 10 00 00 00 14 00 00 00 

This is taken straight from the spec.
'''

EMR_EOF_DUMP = '''000037E0: 0E 00 00 00 14 00 00 00
000037F0:00 00 00 00 10 00 00 00 14 00 00 00 '''

def test_overrun_stuff():
	# This tests the stuff...
	fh = open("testfiles/overrun_thing.txt")
	data = fh.read()
	fh.close()
	# Now try to parse the thing
	spec_data = spec_to_python(data)
	write_to_test_spec_and_import(spec_data) # Try to run the automatic generator...
	bytes_data = parse_hex_dump(EMR_EOF_DUMP)
	eof_obj = cur_module.EMR_EOF(bytes_data)
	# Now check for the fields part.
	# assert 
	print(eof_obj.fields)
	assert eof_obj.fields == ['Type', 'nPalEntries', 'offPalEntries', 'SizeLast'] # The fields should be these.
	good("test_overrun_stuff passed!")
	return

def run_tests():
	test_overrun_stuff()
	return

if __name__=="__main__":

	run_tests()
	exit(0)





