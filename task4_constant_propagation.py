from common import *
import copy

def defaultVariables(graph, defaultValue): #returns a list of all the variables used in the code, initialises them to be == 0
	variables = {}

	for node in graph:
		if node[-1] != ':' and node.split()[1].lower() not in ['if', 'goto', 'return']:
			variables[node.split()[1]] = defaultValue

	return variables

def meet(env1, env2):
	newEnv = {}
	newEnv = env2

	for variable in env1:
		if str(env1[variable]) == str(env2[variable]) or env2[variable] == 'init':
			newEnv[variable] = env1[variable]
#		elif env2[variable] == 'init':
#			newEnv[variable] = env1[variable]
		else:
			newEnv[variable] = 'T'

	return newEnv

def constantFolding(statement): #simplifies a statement using constant folding
	pass

def getNextLine(statement, graph): #gets the next line the code should go to
	for successor in graph[statement]:
		succ = successor.split()
		if succ[1] != 'goto' and succ[-1] != ':':
			return successor

def applyTransferFunction(env, statement, graph): #returns a list of the next statement(s) and environment to be evaluated with the new environment of variables

	#special case if
##############

	operations = ['+', '-', '*', '/']
	newEnv = env		
	TMapping = False

	if statement.split()[2] == '=': #handles '=' case
		splitStatement = statement.split()
		currentPos = 3
		for expr in splitStatement[3:]:
			if expr in env: #handles cases where expr is a variable
				if env[expr] == 'T': 
					#expr is a variable, but is a non-constant
					newEnv[splitStatement[1]] = 'T'
					TMapping = True
					break
				else:
					splitStatement[currentPos] = str(env[expr])
			else: #handles cases where expr is a constant
				if expr not in operations:
					splitStatement[currentPos] = str(expr)

			currentPos += 1

		#applies the operation
	if not TMapping:
		newEnv[splitStatement[1]] = eval(''.join(splitStatement[3:]))
		
	nextStatement = getNextLine(statement, graph)

	if nextStatement.split()[1] == 'EOF':
		return None

	return [(nextStatement, newEnv)]

def processConstants(graph):
	valueMap = {}
	orderedLines = sorted(graph, key = lambda x : int(x.split()[0])) #sorts the code
	
	currentEnvironment = {}
	default = defaultVariables(graph, 'init')
	for node in graph: #initalises each statement to map to blank environment
		currentEnvironment[node] = copy.deepcopy(default)

	if orderedLines[0][-1] == ':':
		statementStack = [(getNextLine(orderedLines[0], graph), defaultVariables(graph, 0))]
	else:
		statementStack = [(orderedLines[0], defaultVariables(graph, 0))]
	
	while statementStack:
		
		currentStatement = statementStack.pop()
#		print currentStatement

		transferFunc = currentStatement[0] #the current statement it's dealing with
		mappings = currentStatement[1] #the variable environment passed from predeccessor

		if mappings == currentEnvironment[transferFunc]: #terminating condition, no more changes can be made or if EOF is reached with no other statements
			return constantPropagation(currentEnvironment)
		
		meetResult = meet(mappings, currentEnvironment[transferFunc])
#		print meetResult
		newStatements = applyTransferFunction(copy.deepcopy(meetResult) , transferFunc, graph)

		if newStatements: #doesn't add if it's EOF
			currentEnvironment[transferFunc] = meetResult
#			print currentEnvironment
			statementStack += newStatements
	
	return constantPropagation(currentEnvironment)

def constantPropagation(variableEnvironment): #replaces variables with constants, returns code as a string
	
	for v in variableEnvironment:
		print v, variableEnvironment[v]


if __name__ == "__main__":
	graph = parse(testinput2)
	processConstants(graph)
#	print applyTransferFunction({'a' : 2, 'b' : 'T', 's' : 'T'}, '3 b = s + a', graph)
#	print meet({'a' : 'T', 'b' : 5}, {'a' : 3, 'b' : 5})	

	
