from common import *
from task1_control_flow_graph import *
from task2_unreachable_code_elimination import *
from task3_jump_elimination import *
from task4_constant_propagation import *
from task6_integration_of_optimisation import *

def	optimiseAll(graph):
	
	optCode = []
#	while len(optCode[-1])oh >
	print '-------------------------------'	
	print 'original code'
	print optimisedCode(graph)
	print
	print '-------------------------------'

	print 'trimming unreachable code'
	task2 = trimNodes(graph)
	task2 = optimisedCode(task2)
	print task2
	print
	print '-------------------------------'
	
	print 'optimising jumps'
	task3 = jump_elimination(task2)
#	task3 = task2
	print task3
	print 
	print '-------------------------------'

	print 'constant propagation and folding'
	task4 = processConstants(task3)
	print optimisedCode(task3)
	print

	print '-------------------------------'
	print 'dead code elimination'
	task5 = task4
	print
	print '-------------------------------'

if __name__ == "__main__":
	optimiseAll(parse(testinput))
