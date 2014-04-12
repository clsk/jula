class Node(object):
    ASSIGNMENT = 0
    IDENTIFIER = 1
    ARGS = 2
    FUNC = 3
    FUNC_CALL = 4
    OP = 5
    IF = 6

    def __init__(self, t, children=[]):
        self.children = children
        self.t = t

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
