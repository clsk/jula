import sys
from tokenizer import Tokenizer
from tokenizer import Token
from parser import Parser

if (__name__ == "__main__"):
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
    parser.parse()
