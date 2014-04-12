from node import *

def get_generator(node):
    if node.t == Node.BLOCK:
        return GeneratorBlock(node)
    elif node.t == Node.ASSIGNMENT:
        return GeneratorAssign(node)
    elif node.t == Node.IDENTIFIER:
        return GeneratorIdentifier(node)
    elif node.t == Node.ARGS:
        return GeneratorArgs(node)
    elif node.t == Node.FUNC:
        return GeneratorFunc(node)
    elif node.t == Node.FUNC_CALL:
        return GeneratorFuncCall(node)
    elif node.t == Node.OP:
        return GeneratorOp(node)
    elif node.t == Node.IF:
        return GeneratorIf(node)
    elif node.t == Node.CONST_LITERAL:
        return GeneratorConstLiteral(node)
    elif node.t == Node.INDEXING:
        return GeneratorIndexing(node)
    elif node.t == Node.OBJ_LITERAL:
        return GeneratorObjectLiteral(node)

class Generator(object):
    def __init__(self, node):
        self.node = node

class GeneratorBlock(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        out = ''
        for child in self.node.children:
            if child is not None:
                out += get_generator(child).generate()
                if child.t != Node.IF and child.t != Node.FUNC:
                    out += ';\n'
        return out

class GeneratorAssign(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return GeneratorIdentifier(self.node.children[0]).generate() + " = " + get_generator(self.node.children[1]).generate()

class GeneratorIdentifier(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return self.node.name

class GeneratorArgs(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        out = ''
        for arg in self.node.children:
            out += get_generator(arg).generate() + ','
        if arg:
            out = out[:-1] # remove last comma

        return out

class GeneratorFunc(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return 'function ' + GeneratorIdentifier(self.node.children[0]).generate() + '( ' + GeneratorArgs(self.node.children[1]).generate() + ') {\n' + GeneratorBlock(self.node.children[2]).generate() + '}\n'

class GeneratorFuncCall(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return GeneratorIdentifier(self.node.children[0]).generate() + '( ' + GeneratorArgs(self.node.children[1]).generate() + ')'

class GeneratorOp(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        if self.node.n == 1:
            out = self.node.op + ' ' + get_generator(self.node.children[0]).generate()
        elif self.node.n == 2:
            out = get_generator(self.node.children[0]).generate() + ' ' + self.node.op + ' ' + get_generator(self.node.children[1]).generate()
        return out

class GeneratorIf(Generator):
    def __init__(self, node, ifelse=False):
        Generator.__init__(self, node)
        self.ifelse

    def generate(self):
        out = 'if ( ' + self.node.children[0] + ' ) {\n' + GeneratorBlock(self.node.children[1]).generate()
        if ifelse:
            out.insert(0, 'else ')

        for i in (2, len(self.node.children)):
            if self.node.children[i] == Node.IF:
                GeneratorIf(self.node.children[i], True)
            else:
                out += 'else \n{ ' + GeneratorBlock(self.node.children[i]).generate() + '\n }'
        return out

class GeneratorConstLiteral(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return self.node.literal

class GeneratorIndexing(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        return GeneratorIdentifier(self.node.children[0]).generate() + '[' + get_generator(self.node.children[1]).generate() + ']'

class GeneratorObjectLiteral(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        out = '{ \n'
        for child in self.node.children:
            out += GeneratorIdentifier(child.children[0]).generate() + ': ' + get_generator(child.children[1]).generate() + ',\n'
        if child:
            out = out[:-2] # remove last comma
        out += '}'
        return out
