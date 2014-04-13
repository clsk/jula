class Node(object):
    ASSIGNMENT = 0
    IDENTIFIER = 1
    ARGS = 2
    FUNC = 3
    FUNC_CALL = 4
    OP = 5
    IF = 6
    INDEXING = 7
    CONST_LITERAL = 8
    OBJ_LITERAL = 9
    BLOCK = 10
    FOR = 11
    WHILE = 12
    REPEAT = 13

    def __init__(self, t, children=[]):
        self.children = children
        self.t = t

class NodeBlock(Node):
    def __init__(self, statements):
        Node.__init__(self, Node.BLOCK, statements)

class NodeIdentifier(Node):
    def __init__(self, name):
        Node.__init__(self, Node.IDENTIFIER)
        self.name = name

class NodeAssignment(Node):
    def __init__(self, lhs, rhs):
        Node.__init__(self, Node.ASSIGNMENT, [lhs, rhs])

class NodeArgumentList(Node):
    def __init__(self, identifiers):
        Node.__init__(self, Node.ARGS, identifiers)

class NodeFunction(Node):
    def __init__(self, name, args, body):
        Node.__init__(self, Node.FUNC, [name, args, body])

class NodeFunctionCall(Node):
    def __init__(self, name, args):
        Node.__init__(self, Node.FUNC_CALL, [name, args])

class NodeOperator(Node):
    def __init__(self, op, n, args):
        Node.__init__(self, Node.OP, args)
        self.op = op
        self.n = n

class NodeIf(Node):
    def __init__(self, condition, block):
        Node.__init__(self, Node.IF, [condition, block])

class NodeIndexing(Node):
    def __init__(self, identifier, exp):
        Node.__init__(self, Node.INDEXING, [NodeIdentifier(identifier), exp])

class NodeConstLiteral(Node):
    def __init__(self, literal):
        Node.__init__(self, Node.CONST_LITERAL)
        self.literal = literal

class NodeObjectLiteral(Node):
    def __init__(self, assignments):
        Node.__init__(self, Node.OBJ_LITERAL, assignments)

class NodeFor(Node):
    def __init__(self, assign, condition, expr, block):
        Node.__init__(self, Node.FOR, [assign, condition, expr, block])

class NodeWhile(Node):
    def __init__(self, condition, block):
        Node.__init__(self, Node.WHILE, [condition, block])

class NodeRepeat(Node):
    def __init__(self, condition, block):
        Node.__init__(self, Node.REPEAT, [condition, block])
