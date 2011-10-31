from common import *

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
	#for k in graph.keys():
	#	if shouldKill(genkill[k]):
	#		graph.pop(k)
	code = recreate_code(graph)
	return code

def gen_kill(graph):
	return {}

def shouldKill(x):
	pass

def recreate_code(graph):
	return graph

# env vars are {} containing
# in and out sets
def meet(u,v):
	return u

def equalSets(a,b):
	# returns true if all elements of a are in b
	# AND all elements of b are in a
	if all([j in b for j in a]) and all([k in a for k in b]):
		return True
	else:
		return False

if  __name__ == "__main__":
	print testinput3
	print dead_code_elimination(testinput3)
