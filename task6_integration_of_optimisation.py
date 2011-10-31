from common import *
from task1_control_flow_graph import *
from task2_unreachable_code_elimination import *
from task3_jump_elimination import *
from task4_constant_propagation import *
from task6_integration_of_optimisation import *
def optSequence(graph, debug): #takes in original code, runs it though each optimisation
	
	if debug:
		print '--------------------------------'	
		print 'original code'
		print optimisedCode(graph)
		print
		print '--------------------------------'

		print 'trimming unreachable code'
		task2 = trimNodes(graph)
		task2 = optimisedCode(task2)
		print task2
		print
		print '--------------------------------'
		
		print 'optimising jumps'
		task3 = jump_elimination(task2)
	#	task3 = parse(task2)
		print optimisedCode(task3)
		print 
		print '--------------------------------'

		print 'constant propagation and folding'
		task4 = processConstants(task3)
		print optimisedCode(task4)
		print
		print '--------------------------------'

		print 'dead code elimination'
		task5 = optimisedCode(task4)
		print
		print '--------------------------------'
		
	else:
		return optimisedCode	(
								processConstants	(
													jump_elimination	(
																		optimisedCode(trimNodes(graph))
																		)
													)
								)

	return task5

def	optimiseAll(graph, debug = False): #takes in the original graph of the code, prints out each phase of optimisation
#	debug = True
	print '--original code---'
	print optimisedCode(graph)
	print '#of lines =', optimisedCode(graph).count('\n')
	print '######beginning optimisation######'

	optCode = [optSequence(graph, debug)]

	print 'iteration #1'
	print optCode[-1]
	print
	print '#of lines =', optCode[-1].count('\n')
	print '---------------'
	
	optCode += [optSequence(parse(optCode[-1]), debug)]
	print 'iteration #2'
	print optCode[-1]
	print 
	print '#of lines =', optCode[-1].count('\n')
	print '---------------'

	iterationCount = 2
	while optCode[-1].count('\n') < optCode[-2].count('\n'): #hill climbing
		iterationCount += 1
		optCode += [optSequence(parse(optCode[-1]), debug)]
		print 'iteration #' + str(iterationCount)
		print optCode[-1]
		print
		print '#of lines =', optCode[-1].count('\n')
		print '---------------'

	print '-----last iteration reached-----'
	print optCode[-1]
	print
	print '#of lines =', optCode[-1].count('\n')

	return optCode[-1]

if __name__ == "__main__":
	optimiseAll(parse(testinput3))
