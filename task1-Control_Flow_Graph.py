from sample1 import *

def parse(code): #takes in code, outputs the control flow graph in dictionary form

	tokens = {} #maps the unique line + code to it's successors in the graph
	lastadded = '' #contains the last added entry to the token dictionary

	mapping = [] #contains the ordered, by line numbers, list of tokens (for convenience)
	labelMatch = {}	#contains the mappings of the line of code to the processed line, i.e. 'L1:' --> '8 L1:' (for convenience)

	temptokens = code.replace(':', ':;').split(';')[:-1]

	for token in range(len(temptokens) + 1)[1:]:
	
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
				tokens[token] += tokens[successor]
				tokens[token] = list(set(tokens[token])) #uniques the list
				
				if lengthBefore < len(tokens[token]): #checks if list has actually been changed
					changes = True

			elif successor[-1] == ':': #special case when a label follows another label
				lengthBefore = len(tokens[token])
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
def toDotFormat(tokens):
	print """
/*
* @command = dot
*
*/
digraph g {
rankdir = LR
a -> b ;
a -> c ;
a -> d ;
a -> e;
"a = 2" -> f;
f -> a;
} 
	"""

if __name__ == "__main__":
	toDotFormat(parse(testinput))
