from node import *
from tokenizer import *

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.pos = -1

    def parse(self):
        if not self.tokenizer.tokenized:
            self.tokenizer.tokenize()

        self.tokens = self.tokenizer.tokens
        block = self.parse_block()
        if self.pos != len(self.tokens):
            self.flag_error("Input reached end of file")
        return block

    def parse_block(self, terminator = Token.END):
        print "parsing block"
        statements = []
        t = self.get_token()
        while t != None and t.t != terminator:
            statements.append(self.parse_statement())
            t = self.get_token()

        return NodeBlock(statements)
        print "done parsing block"

    def parse_arg_list(self):
        print "parsing arg list"
        if self.current_token().t != Token.LPAREN:
            self.flag_error("Expecting left parenthesis at parse_arg_list")

        ids = []
        t = self.get_token()
        while t.t == Token.IDENTIFIER:
            ids.append(NodeIdentifier(t.text))
            t = self.get_token()
            if t.t == Token.RPAREN:
                break
            elif t.t != Token.COMMA:
                self.flag_error("Expected comma or closing parenthesis at parse_arg_list")

            t = self.get_token()

        return NodeArgumentList(ids)

    def parse_arg_call_list(self, beginning = Token.LPAREN, terminator = Token.RPAREN):
        print "parsing arg call list"
        if self.current_token().t != beginning:
            self.flag_error("Expecting left parenthesis at parse_arg_list")

        t = self.get_token()
        ids = []
        if (t.t != terminator):
            while t.t != None:
                ids.append(self.parse_expression())
                t = self.get_token()
                if t.t == terminator:
                    break
                elif t.t != Token.COMMA:
                    self.flag_error("Expected comma or closing parenthesis at parse_arg_call_list")
                t = self.get_token()

        return NodeArgumentList(ids)

    def parse_func(self):
        print "parsing func"
        t = self.get_token()
        if t.t != Token.IDENTIFIER:
            self.flag_error("Expecting function name")
        name = NodeIdentifier(t.text)

        t = self.get_token()
        args = self.parse_arg_list()
        return NodeFunction(name, args, self.parse_block())

    def parse_statement(self):
        print "parsing statement"
        token = self.current_token()
        if token.t == Token.IF:
            return self.parse_if()
        elif token.t == Token.FUNCTION:
            return self.parse_func()
        elif token.t == Token.FOR:
            return self.parse_for()
        elif token.t == Token.WHILE:
            return self.parse_while()
        elif token.t == Token.REPEAT:
            return self.parse_repeat()
        else:
            exp =  self.parse_expression()
            if self.get_token().t != Token.SEMICOLON:
                self.flag_error("Expecting semicolon at parse_stement")
            return exp

    def parse_if(self):
        print "parsing if"
        if (self.get_token().t != Token.LPAREN):
            self.flag_error("Expecting opening parenthesis at parse_if")

        self.get_token()
        condition = self.parse_expression()

        if (self.get_token().t != Token.RPAREN):
            self.flag_error("Expecting closing parenthesis at parse_if")

        if self.get_token().t != Token.THEN:
            self.flag_error("Expecting opening then at parse_if")

        block = self.parse_block()
        node = NodeIf(condition, block)
        t = self.get_token()
        while t != None:
            if t.t == Token.ELSEIF:
                node.children.append(self.parse_if())
            else:
                break
            t = self.get_token()

        if t.t == Token.ELSE:
            print "appended else"
            node.children.append(self.parse_else())
        elif t != None:
            self.unget_token()
        return node


    def parse_else(self):
        print "parsing else"
        return self.parse_block()

    def parse_object_literal(self):
        print "parsing object literal"
        assignments = []
        t = self.get_token()
        while t.t == Token.IDENTIFIER:
            assignments.append(self.parse_object_literal_assign())
            t = self.get_token()
            if t.t == Token.RCURLY:
                break
            elif t.t != Token.COMMA:
                self.flag_error("Expected comma or closing parenthesis at parse_object_literal")

            t = self.get_token()

        # Make sure current_token is RCURLY
        if self.current_token().t != Token.RCURLY:
            self.flag_error("Expecting clusing curly brace at parse_object_literal")
        return NodeObjectLiteral(assignments)

    def parse_for(self):
        self.get_token() # consume for
        assign = self.parse_arg_call_list(Token.LPAREN, Token.SEMICOLON)

        t = self.get_token()
        if t.t == Token.SEMICOLON:
            condition = None
        else:
            condition = self.parse_expression()
            if self.get_token().t != Token.SEMICOLON:
                self.flag_error("Expecting semicolon after condition at parse_for")

        exprs = self.parse_arg_call_list(Token.SEMICOLON, Token.RPAREN)

        block = self.parse_block()
        return NodeFor(assign, condition, exprs, block)

    def parse_while(self):
        if self.get_token().t != Token.LPAREN:
            self.flag_error("Expecting opening parenthesis at while")

        self.get_token()

        condition = self.parse_expression()

        if self.get_token().t != Token.RPAREN:
            self.flag_error("Expecting closing parenthesis at while")

        if self.get_token().t != Token.DO:
            self.flag_error("Expecting do directive in parse_while")
        return NodeWhile(condition, self.parse_block())

    def parse_repeat(self):
        print "parsing repeat"
        print self.current_token().text
        block = self.parse_block(Token.UNTIL)

        if self.get_token().t != Token.LPAREN:
            self.flag_error("Expecting opening parenthesis at parse_repeat")

        self.get_token()

        condition = self.parse_expression()

        if self.get_token().t != Token.RPAREN:
            self.flag_error("Expecting closing parenthesis at parse_repeat")

        if self.get_token().t != Token.SEMICOLON:
            self.flag_error("Expecting semicolon in parse_repeat")
        return NodeRepeat(condition, block)


    def parse_object_literal_assign(self):
        print "parsing object literal assignment"
        identifier = self.current_token().text
        print "identifier: " + identifier
        if self.get_token().t != Token.COLON:
            self.flag_error("Expecting colon at parse_object_literal_assign")
        self.get_token() # consume colon
        return NodeAssignment(NodeIdentifier(identifier), self.parse_expression())

    def parse_expression(self):
        print "parsing expression"
        op = None
        left = None
        node = None
        t = self.current_token()
        while t != None:
            if t.t == Token.RPAREN or t.t == Token.RBRACK or t.t == Token.RCURLY or t.t == Token.SEMICOLON or t.t == Token.COMMA:
                self.unget_token()
                break
            elif t.t == Token.LPAREN:
                self.get_token()
                left = self.parse_expression()
                if self.get_token().t != Token.RPAREN:
                    self.flag_error("Expecting closing parenthesis")
            elif t.t in Tokenizer.prefix_operators:
                self.get_token()
                return NodeOperator(t.text, 1, [self.parse_expression()])
            elif left is None:
                if t.t == Token.NUMBER or t.t == Token.STRING or t.t == Token.TRUE or t.t == Token.FALSE or t.t == Token.IDENTIFIER or t.t == Token.LCURLY:
                    if t.t == Token.IDENTIFIER:
                        p = self.peak_token()
                        if p.t == Token.LPAREN: # this is a function call
                            left = self.parse_func_call()
                        elif p.t == Token.LBRACK:
                            left = self.parse_indexing()
                        else:
                            left = NodeIdentifier(t.text)
                    elif t.t == Token.LCURLY:
                        left = self.parse_object_literal()
                    else:
                        left = NodeConstLiteral(t.text)
                else:
                    self.flag_error("Expecting literal or identifier in parse_expression")
            elif t.t in Tokenizer.binary_operators:
                self.get_token()
                right = self.parse_expression()
                node = NodeOperator(t.text, 2, [left, right])
                left = None
                break
            else:
                self.flag_error("Unexpected token at parse_expression")
            t = self.get_token()

        print "ended parsing expression"
        if left is not None:
            return left
        elif node is not None:
            return node
        else:
            self.flag_error("Expecting something at parse_expression")

    def parse_func_call(self):
        print "parsing func call"
        name = self.current_token().text
        self.get_token()
        args = self.parse_arg_call_list()
        return NodeFunctionCall(NodeIdentifier(name), args)

    def parse_indexing(self):
        print "parsing indexing"
        identifier = self.current_token().text
        self.get_token() # consume left bracket
        self.get_token()
        exp = self.parse_expression()
        if (self.get_token().t != Token.RBRACK):
            self.flag_error("Expecting closing bracket at parse_indexing")

        return NodeIndexing(identifier, exp)

    def get_token(self):
        if self.pos+1 < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos]
        else:
            self.pos = len(self.tokens)
            return None

    def current_token(self):
        return self.tokens[self.pos]

    def unget_token(self):
        self.pos -= 1

    def peak_token(self):
        if self.pos+1 < len(self.tokens):
            return self.tokens[self.pos+1]

    def flag_error(self, s):
        print "Error: " + repr(self.current_token().lineno) + ":" + repr(self.current_token().column) + ": " + s + ". instead received (" + repr(self.current_token().t) + ") " + self.current_token().text
        exit()
