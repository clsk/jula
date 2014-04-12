import sys
from tokenizer import Tokenizer
from tokenizer import Token
from parser import Parser
from generator import *

if (__name__ == "__main__"):
    outfile = 'out.js'
    if len(sys.argv) < 2:
        print "Error: Missing input file argument!"
        exit(0)

    it = iter(sys.argv)
    it.next() # Skip this file
    for arg in it:
        if (arg == "-o"):
            outfile = it.next()
        elif arg == "-h":
            print "Syntax: \npython jula.py <infile.jula> [-o outfile.js]"
            quit()
        else:
            infile = arg

    if (infile == None):
        print "Error: Missing input file argument!"
        quit()

    print "Scanning:", infile + "..."


    t = Tokenizer(infile)
    t.tokenize()
    for token in t.tokens:
        print repr(token.lineno) + ":" + repr(token.column) + ": (" + repr(token.t) + ") " + token.text
    print "Beginning parse process..."
    parser = Parser(t)
    ast = parser.parse()
    output = get_generator(ast).generate()
    with open(outfile, "w") as out:
        out.write(output)
