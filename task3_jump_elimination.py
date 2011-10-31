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
	code = optimized_code(code,useless_jump)
	code = optimized_code(code,jump_to_jump)
	code = optimized_code(code,cond_to_jump)
	code = optimized_code(code,jump_to_cond)
	# takes some code, eliminates the jumps, then outputs the new code
	print code
	return parse(code)

def optimized_code(code,optimization):
	# this function will take an optimization and
	# run it over the code, returning the new code
	lines = code.split("\n")
	lines = map(lambda xs: xs.strip(), lines)
	lines = filter(lambda xs: len(xs) > 0, lines)
	graph = parse(code)
	optimizedCode = ""
	ln = 1 # linenumber
	for line in lines:
		newline = optimization(graph,line,ln)
		optimizedCode += newline + "\n"
		ln += 1
	# takes some code, eliminates the jumps, then outputs the new code
	return optimizedCode

def jump_to_jump(graph,line,ln):
	# A "jump_to_jump" optimization will match the template
	#	line = "goto LX", where LX is a Label
	# and
	#	"LX: \ngoto LY", where LY is a Label
	splitline = line.split()
	if len(splitline) == 2 and splitline[0].lower() == "goto":
		# from this point we know it's a goto line
		# need to check if it's going to another goto
		lineWithNumber = getLine(line,ln)
		if lineWithNumber:
			number = lineWithNumber.split()[0]
			label = splitline[1]
			for l in graph[lineWithNumber]:
				sl = l.split()
				if len(sl) == 3 and sl[1].lower() == "goto":
					optimizedLine = " ".join(["goto",sl[2]])+ ";"
					return optimizedLine
	return line

def jump_to_cond(graph,line,ln):
	# A "jump_to_cond" optimization iwll match the template
	#	line = "goto LX"
	# and
	#	"LX: \nif expr goto LY"
	# and make it
	#	 "if expr goto LY"
	splitline = line.split()
	if len(splitline) == 2 and splitline[0].lower() == "goto":
		# from this point we know it's a goto line
		# need to check if it's going to an 'if expr goto LY'
		lineWithNumber = getLine(line,ln)
		if lineWithNumber:
			number = lineWithNumber.split()[0]
			label = splitline[1]
			for l in graph[lineWithNumber]:
				sl = l.split()
				#TODO make this work on expressions properly
				if sl[1].lower() == "if" and sl[3].lower() == "goto":
					return " ".join(sl[1:]) + ";"
	return line

def useless_jump(graph,line,ln):
	# A "useless_jump" is a jump that has a 'goto' that points 
	# to the next line
	splitline = line.split()
	if len(splitline) == 2 and splitline[0].lower() == "goto":
		thisLine = getLine(line,ln)
		if thisLine:
			for target in graph[thisLine]:
				if target.split()[0] == str(ln+1):
					return ""
	return line

def cond_to_jump(graph,line,ln):
	# A "cond_to_jump" is a conditional goto to another goto
	# and will optimize to a conditional jump to the second goto
	splitline = line.split()
	if len(splitline) >= 4 and splitline[0].lower() == "if" and splitline[2].lower() == "goto":
		# Then this is a conditional jump
		# and we need to check if it's jumping to another jump
		thisLine = getLine(line,ln)
		# get the label linenumber
		for target in graph[thisLine]:
			if splitline[-1][:-1] == target.split()[-1][:-1]:
				linenumber = target.split()[0]
				break
		# get the line after the label
		for target in graph[thisLine]:
			if target.split()[0] == str(1+int(linenumber)):
				nextline = target
				if nextline.split()[-2] == "goto":
					return " ".join(splitline[0:2]+nextline.split()[1:]) + ";"
	return line

def getCode(line):
	print splitline
	# the code is stored as a string with the line number at the head.
	# this function returns the code (strips the linenumber)
	return " ".join(line.split()[1:])

def getLine(line,ln):
	return str(ln) + " " + line[:-1] # strips a semicolon off the line


if __name__ == "__main__":
	#inp = testinput
	#inp = testinput2
	#inp = testinput3
	#inp = testinput4
	#inp = testinput5
	inp = testinput6
	print inp
	print "******************"
	optCode = jump_elimination(inp)
	print "******************"
	print optCode
