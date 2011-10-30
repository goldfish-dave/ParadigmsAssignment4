from common import *

###
# Jump elimination optimization works by searching the code, matching jump templates.
# if it matches a jump template it then replaces the code with optimized code.
#
# There are four templates used in this optimization:
#	* jumps to jumps
#	* jumps to conditional jumps
#	* useless jumps
#	* conditional jumps to jumps
#
# Which can be optimized to:
#	* a single jump
#	* a conditional jump 
#	* no jumps 
#	* a conditional jump
# respectively.
#
# The following code implements all four cases as individual functions that take a graph 
# and a line and return the (potentially optimized) line. All optimizations are performed
# on all lines and grouped in the function jump_elimination(graph).

def jump_elimination(code):
	lines = code.split("\n")
	graph = parse(code)
	optimizedCode = "\n".join([optimized_line(graph,line) for line in lines])
	# takes some code, eliminates the jumps, then outputs the new code
	return optimizedCode

def optimized_line(graph,line):
	opt0 = jump_to_jump(graph,line)
	opt1 = jump_to_cond(graph,opt0)
	opt2 = useless_jump(graph,opt1)
	opt3 = cond_to_jump(graph,opt2)
	return opt3

def jump_to_jump(graph,line):
	# A "jump_to_jump" optimization will match the template
	#	line = "goto LX", where LX is a Label
	# and
	#	"LX: \ngoto LY", where LY is a Label
	
	splitline = line.split()
	if len(splitline) == 2 and splitline[0].lower() == "goto":
		# from this point we know it's a goto line
		# need to check if it's going to another goto
		lineWithNumber = getLine(graph,line)
		if lineWithNumber:
			number = lineWithNumber.split()[0]
			label = splitline[1]
			print number, label
			for l in graph[lineWithNumber]:
				sl = l.split()
				if len(sl) == 3 and sl[1].lower() == "goto":
					optimizedLine = " ".join(["goto",sl[2]])+ ";"
					print optimizedLine
					return optimizedLine


	return line

def jump_to_cond(graph,line):
	return line

def useless_jump(graph,line):
	return line

def cond_to_jump(graph,line):
	return line

def getCode(line):
	print splitline
	# the code is stored as a string with the line number at the head.
	# this function returns the code (strips the linenumber)
	return " ".join(line.split()[1:])

def getLine(graph,line):
	# returns the first occurance of line in graph
	for k in graph.keys():
		#print str(" ".join(k.split()[1:])) + " AND " + str(line[:-1])
		if " ".join(k.split()[1:]) == line[:-1]:
			#print "MATCH: ", k
			return k
	return None

def getLineByNumber(code,number):
	return code.split("\n")[number]

if __name__ == "__main__":
	print testinput3
	print "******************"
	optCode = jump_elimination(testinput3)
	print "******************"
	print optCode
