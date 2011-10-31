from common import *
import copy

def defaultVariables(graph, defaultValue): #returns a list of all the variables used in the code, initialises them to be == 0
	variables = {}

	for node in graph:
		if node[-1] != ':' and node.split()[1].lower() not in ['if', 'goto', 'return']:
			variables[node.split()[1]] = defaultValue

	return variables

def meet(env1, env2): #calculates the meet of 2 environment variables. x ^ x = x, x ^ y = T, T ^ x = T
#	newEnv = {}
	newEnv = copy.deepcopy(env2)
#	print env1, env2
	for variable in env1:
		if str(env1[variable]) == str(env2[variable]) or (env2[variable] == 'init' and env1[variable] != 'T'):
			newEnv[variable] = env1[variable]
		else:
			newEnv[variable] = 'T'

	return newEnv

def constantFolding(statement): #simplifies a statement using constant folding
#	print statement
	RHS = statement.split()[3:]
	LHS = statement.split()[:3]
	operations = ['+', '-', '*', '/']
	for token in RHS:
		if not token.isdigit() and token not in operations:
			return statement

	return ' '.join(LHS) + ' ' + str(eval(' '.join(RHS)))	

def getNextLine(statement, graph): #gets the next line the code should go to

	if statement not in graph: #finds '<line> L1:' when given 'L1:'
		for successor in graph:
			if successor.split()[1] == statement:
				statement = successor

	for successor in graph[statement]:
		succ = successor.split()
		if succ[1] != 'goto' and successor[-1] != ':':
			return successor

def applyTransferFunction(env, statement, graph): #returns a list of the next statement(s) and environment to be evaluated with the new environment of variables
	
#	print env, statement
	#case for return

	newEnv = env		
	
	if statement.split()[1].lower() == 'return': #checks for return, return does not have anything following it
		return [(statement, env)]

	if statement.split()[1].lower() == 'if':
		if env[statement.split()[2]] == True: #if condition always maps to True then go to label
			newEnv[statement.split()[2]] = True
			return[(getNextLine(statement.split()[4] + ':', graph), newEnv)]

		elif env[statement.split()[2]] == False: #if condition always maps to False then go to next line
			newEnv[statement.split()[2]] = False
			for successor in graph[statement]: #gets the next line, skipping the goto
				succ = successor.split()

				if int(succ[0]) == int(statement.split()[0]) + 1: #manually scans for the next line
					if succ[1] == 'goto' or successor[-1] == ':': #if it's a label or a goto, then jump to next possible line
						return [(getNextLine(successor, graph), newEnv)]
					else:
						return [(successor, newEnv)]

		elif env[statement.split()[2]] == 'T' : #if condition cannot be evaluated then go to both
			newEnv[statement.split()[2]] = True
			newEnvTrue = newEnv

			newEnvFalse = copy.deepcopy(env)
			newEnvFalse[statement.split()[2]] = False
			for successor in graph[statement]:
				succ = successor.split()
				if int(succ[0]) == int(statement.split()[0]) + 1:
					if succ[1] == 'goto' or successor[-1] == ':':
						return	[
								(getNextLine(statement.split()[4] + ':', graph), newEnvTrue)
								, (getNextLine(sucessor, graph), newEnvFalse)
								]
					else:
#						print '----'
#						print [
#								(getNextLine(statement.split()[4] + ':', graph), newEnvTrue)
#								, (successor, newEnvFalse)
#								]

						return	[
								(getNextLine(statement.split()[4] + ':', graph), newEnvTrue)
								, (successor, newEnvFalse)
								]
		return None #'EOF' case
##############

	operations = ['+', '-', '*', '/']
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

	#applies the operation, if the variable doesn't map to T
	if not TMapping:
		newEnv[splitStatement[1]] = eval(''.join(splitStatement[3:]))
	
#	print 'here', newEnv
	nextStatement = getNextLine(statement, graph)

	if nextStatement.split()[1] == 'EOF': #special case for EOF
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
#		print '--', currentStatement

		transferFunc = currentStatement[0] #the current statement it's dealing with
		mappings = currentStatement[1] #the variable environment passed from predeccessor

		if mappings == currentEnvironment[transferFunc]: #terminating condition, no more changes can be made or if EOF is reached with no other statements
#			return constantPropagation(currentEnvironment)
			continue
		
		meetResult = meet(mappings, currentEnvironment[transferFunc])
#		print meetResult
		newStatements = applyTransferFunction(copy.deepcopy(meetResult) , transferFunc, graph)


		if newStatements: #doesn't add if it's EOF
			currentEnvironment[transferFunc] = meetResult #updates the environment variables for that particular line/statement

			if newStatements[-1][0].split()[1] != 'return': #specific case for return values
				statementStack += newStatements

			else: #updates environment variables for the return line, but doesn't add it to the stack to be processed
				currentEnvironment[newStatements[0][0]] = newStatements[0][1]

	return constantPropagation(currentEnvironment)

def constantPropagation(variableEnvironment): #replaces variables with constants, returns code as a string
	
	code = []
	
	for v in sorted(variableEnvironment):
		print v, variableEnvironment[v]

	for statement in variableEnvironment:
		
		currentState = variableEnvironment[statement]
		tokens = statement.split()
		if tokens[1] == 'if':
			if currentState[tokens[2]] == 'T':
				code += [statement]

			elif currentState[tokens[2]] == True: #always true
				code += [' '.join([statement.split()[0]] + statement.split()[3:])] 

			#else ignore line since it always evaluates to false, if b goto L1: -> ' ', where b is a constant mapping to False

		elif tokens[1] == 'return': 
			if currentState[tokens[2]] not in ['T', 'init']:
				if currentState[tokens[2]] in [True, False]: #the return value can also be true/false as well as an integer
					code += [statement] #return b -> return b, even if b is a constant boolean
				else: #return x -> return 10, if x is a constant which maps to 10
					statement = ' '.join	(
											tokens[:-1]
											+ [str(currentState[tokens[2]])]
											)

					code += [statement]
			else:
				code += [statement]
		elif tokens[1] == 'goto' or statement[-1] == ':':
			code += [statement]

		else:
			tokenPlace = 3
			for token in tokens[3:]:
#				print statement
				if token in currentState:
					if currentState[token] not in ['T', 'init']:
						#substitutes constant in for variable
						statement = ' '.join	(
												tokens[:tokenPlace] 
												+ [str(currentState[token])] 
												+ tokens[tokenPlace + 1:]
												)

				tokenPlace += 1

			#constant folding
			statement = constantFolding(statement)

			code += [statement]		
#	print code	
	return optimisedCode(code)
if __name__ == "__main__":
	graph = parse(testinput3)
	print processConstants(graph)
#	toDotFormat(parse(processConstants(graph)))
#	toDotFormat(parse(processConstants(graph)))

#	print toDotFormat(processConstants(graph))
#	print applyTransferFunction({'a' : 2, 'b' : 'T', 's' : 'T'}, '3 b = s + a', graph)
#	print meet({'a' : 'T', 'b' : 5}, {'a' : 3, 'b' : 5})	

	
