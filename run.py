import sys

import antlr3
from build.JumpLexer import JumpLexer
from build.JumpParser import JumpParser

def main(filename):
	char_stream = antlr3.ANTLRFileStream(filename)
	tokens = antlr3.CommonTokenStream(JumpLexer(char_stream))
	parser = JumpParser(tokens)
	graph = parser.prog().graph

	while True:
		graph.construct()
		#graph.print_CFG(sys.stdout)
		if graph.perform_JE():
			continue
		if graph.perform_UC():
			continue
		if graph.perform_CP():
			continue
		if graph.perform_DCE():
			continue
	
	graph.print_source(sys.stdout)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print >> sys.stderr, "Usage: %s <filename" % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
