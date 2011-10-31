from common import *

#TODO complete this task ...
# currently dead_code_elimination is a computationally expensive null op

# This section uses the fixed-point solution of the dead_code_elimination
# algebraic relation:
#	M(n)[x] = (x-kill(n)) ++ gen(n)
# 
# It does this by initializing a dictionary of (in,out) tuples (each are list/sets)
# and recomputing them in a loop until they stop changing.

def dead_code_elimination(code):
	# create genkill set
	# for each key, if it's in the killset, pop it from graph
	# from the graph left over, recreate the code
	graph = parse(code)
	genkill = gen_kill(graph)
	for k in graph.keys():
		if shouldKill(genkill[k]):
			graph.pop(k)
	code = recreate_code(graph)
	return code

def gen_kill(graph):
	genkill = {}
	for k in graph.keys():
		genkill[k] = ([],[]) # (gen,kill)
	return genkill

def shouldKill(x):
	return False

def recreate_code(graph):
	num_line = [ (k.split()[0], " ".join(k.split()[1:])) for k in graph.keys() ]
	sorted_num_line = sorted(num_line,key=lambda nl:int(nl[0]))
	lines = "\n".join([line for (num,line) in sorted_num_line])
	return lines

if  __name__ == "__main__":
	print testinput3
	print "******"
	print dead_code_elimination(testinput3)
	print "******"
