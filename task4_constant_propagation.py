from common import *

def processConstants(graph):
	valueMap = {}
	orderedLines = sorted(graph, key = lambda x : int(x.split()[0])) #sorts the code

	for node in orderedLines:
		print node
	
if __name__ == "__main__":
	graph = parse(testinput2)
	processConstants(graph)
