from sample import *
from task1_control_flow_graph import *

def parse(code): #takes in code, outputs the control flow graph in dictionary form (provides a bridge for cases with goto's and labels)

	tokens = {} #maps the unique line + code to it's successors in the graph
	lastadded = '' #contains the last added entry to the token dictionary

	mapping = [] #contains the ordered, by line numbers, list of tokens (for convenience)
	labelMatch = {}	#contains the mappings of the line of code to the processed line, i.e. 'L1:' --> '8 L1:' (for convenience)

	temptokens = code.replace(':', ':;').split(';')[:-1]

	for token in range(len(temptokens) + 1)[1:]: #puts the code into a dictionary data type, node -> direct successors
		lastadded = str(token) + ' ' + temptokens[token - 1].strip()
		tokens[lastadded] = []
		mapping += [lastadded]
		labelMatch[temptokens[token - 1].strip()] = lastadded
	
	mapping += [str(len(temptokens) + 1) + ' EOF']

	changes = True
	while changes: #do until no more successors can be added to the token dictionary
		changes = False
		for token in tokens:

			successor = mapping[int(token.split()[0])]

			if token.split()[1] == 'goto': #for the case: "goto L1"
				successor = labelMatch[token.split()[2] + ':']
				lengthBefore = len(tokens[token])

				tokens[token] += [successor] ##added
				tokens[token] += tokens[successor]
				tokens[token] = list(set(tokens[token])) #uniques the list
				
				if lengthBefore < len(tokens[token]): #checks if list has actually been changed
					changes = True

			elif successor[-1] == ':' or successor.split()[1] == 'goto': #if a label or a 'goto' statement is the successor
				lengthBefore = len(tokens[token])

				tokens[token] += [successor] ##added
				tokens[token] += tokens[successor]
				tokens[token] = list(set(tokens[token])) #uniques the list
				if lengthBefore < len(tokens[token]): #checks if list has actually been changed
					changes = True
			else:
				if successor not in tokens[token]: #checks for unique entry
					tokens[token] += [successor] #adds next immediate line to successors
					changes = True
			
			if token.split()[1] == 'if': #for the case: "if x goto L1"

				successor = labelMatch[token.split()[4] + ':']
				lengthBefore = len(tokens[token])

				tokens[token] += [successor] ##added
				tokens[token] += tokens[successor]
				tokens[token] = list(set(tokens[token])) #uniques the list
				
				if lengthBefore < len(tokens[token]): #checks if list has actually been changed
					changes = True

	"""
	print '---------------------------------------------------------------'
	for m in mapping:
		print m
	print '---------------------------------------------------------------'
	for x in sorted(list(tokens)):
		print x, '-->', tokens[x]
	"""
	return tokens

def optimisedCode(graph): #takes in the processed code, outputs as normal code (string) in sequential order

	orderedLines = sorted(graph, key = lambda x : int(x.split()[0])) #sorts the code
	unNumbered = map(lambda x : ' '.join(x.split()[1:]), orderedLines) #gets rid of line numbers added in processing
	
	if unNumbered[-1] == 'EOF': #special case for when the last line of the code gets optimised out, nothing points to EOF
		unNumbered = unNumbered[:-1]
	for line in range(len(unNumbered)):
		if unNumbered[line][-1] != ':':
			unNumbered[line] += ';'
			unNumbered[line] = ' ' + unNumbered[line]
	return '\n'.join(unNumbered)
