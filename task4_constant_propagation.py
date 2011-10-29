from common import *

def defaultVariables(graph): #returns a list of all the variables used in the code, initialises them to be == 0
	variables = {}

	for node in graph:
		if node[-1] != ':' and node.split()[1].lower() not in ['if', 'goto', 'return']:
			variables[node.split()[1]] = 0

	return variables

def meet(env1, env2):

	return env1

def constantFolding(statement): #simplifies a statement using constant folding
	pass

def applyTransferFunction(env, statement, graph): #returns a list of the next statement(s) and environment to be evaluated with the new environment of variables
	
	print env
	print statement
	print graph

#	if statement.split().lower()[1] == 'if':
#		pass
	

	newEnv = env		

	if statement.split()[2] == '=':
		splitStatement = statement.split()
		if splitStatement[3] in env:
			newEnv[statement[1]] = env[statement[3]]

		else:
			newEnv[statement[1]	
	#[(statement1, env), (statement2..
	return env

def processConstants(graph):
	valueMap = {}
	orderedLines = sorted(graph, key = lambda x : int(x.split()[0])) #sorts the code
	
	currentEnvironment = {}
	for node in graph: #initalises each statement to map to blank environment
		currentEnvironment[node] = {}

	statementStack = [(orderedLines[0], defaultVariables(graph))]
	
	while statementStack:

		currentStatement = statementStack.pop()
		transferFunc = currentStatement[0]
		mappings = currentStatement[1]

		if mappings == currentEnvironment[currentStatement]: #terminating condition, no more changes can be made
			return constantPropagation(currentEnvironment)

		newStatements = applyTransferFunction(
									meet(
										mappings, currentEnvironment[currentStatement]
										)
									, transferFunc, graph
									)
		statementStack += newStatements

def constantPropagation(variableEnvironment): #replaces variables with constants, returns code as a string
	pass

if __name__ == "__main__":
	graph = parse(testinput2)
#	processConstants(graph)
	applyTransferFunction({'a' : 1, 'b' : 0, 'c' : 0}, '1 a = 0', graph)

	
