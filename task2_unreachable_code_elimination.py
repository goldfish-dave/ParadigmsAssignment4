from common import *
from task1_control_flow_graph import *
from copy import deepcopy
def trimNodes(graph): #removes all the nodes with no existing predecessors
	reachable = [filter(lambda x : x[0:2] == '1 ', graph)[0]] #all reachable nodes, first node is a special case
	nodeStack = reachable #nodes being processed
	
	while nodeStack: #depth first search
		currentnode = nodeStack.pop()
		reachable = deepcopy(reachable)

		if currentnode not in reachable:
			reachable += [currentnode]
			if currentnode in graph: #specialcase for EOF
				nodeStack += graph[currentnode]
	trimmedGraph = {}
	
	for node in graph:
		if node in reachable:
			trimmedGraph[node] = graph[node]

	return trimmedGraph

if __name__ == "__main__":
#	graph = parse(testinput)
	graph = parse(testinput3)

	print 'original code'
	print optimisedCode(graph)
	print
	print 'removing unreachable code'
	opt = trimNodes(graph)
	print optimisedCode(opt)
