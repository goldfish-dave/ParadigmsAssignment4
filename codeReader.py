import sys
from task6_integration_of_optimisation import *

def readCode(filename):
	f = open(filename, 'r')
	
	code = f.read()
	f.close()
	return code

if __name__ == "__main__":
	
	if len(sys.argv) == 1:
		#manual input, read from sample.py
		optimiseAll(parse(testinput10))#, True) #add True as second argument for debug statements
	else: #read from file given as argument
		optimiseAll(parse(readCode(sys.argv[1]))) #,True )
