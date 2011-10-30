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

def jump_elimination(graph):
	# takes a graph, eliminates the jumps, then outputs a new graph
	return graph

def match_template(graph, line): 
	# takes a graph and a line,
	# matches the first possible template (if any),
	# then returns the template matched.
	# if template matches then returns None
	return None

if __name__ == "__main__":
	graph = parse(testinput)
	optGraph = jump_elimination(graph)
	print optGraph
