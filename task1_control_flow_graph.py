from common import *

def toDotFormat(tokens): #converts the dictionary form cfg to DOT langauge
	print """ 
/*
* @command = dot
*
*/
digraph g {
rankdir = LR"""
	
	#The format is as follows : <line in which the code appeared> : <code> 
	for token in tokens:
		if token[-1] != ':' and token.split()[1] != 'goto': #ignores labels and goto's
			for successors in tokens[token]:
				if successors.split()[1] != 'EOF' and successors.split()[1] != 'goto' and successors[-1] != ':': #ignores EOF
					print	('"' 
							+ token.split()[0] + ': ' + ' '.join(token.split()[1:])
							+ '" -> "' 
							+ successors.split()[0] + ': ' + ' '.join(successors.split()[1:])
							+ '"'
							)
	print "}"

if __name__ == "__main__":
#	toDotFormat(parse(testinput))
	toDotFormat(parse(testinput3))
