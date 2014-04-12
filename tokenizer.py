class Token:
    ERROR = -1
    NUMBER = 0
    IDENTIFIER = 1
    RESERVED = 2
    IF = 3
    THEN = 4
    ELSEIF = 5
    ELSE = 6
    SWITCH = 7
    CASE = 8
    FOR = 9
    WHILE = 10
    DO = 11
    UNTIL = 12
    CONTINUE = 13
    BREAK = 14
    IN = 14
    NIL = 15
    NOT = 16
    END = 17
    AND = 18
    OR = 19
    TRUE = 20
    FALSE = 21
    RETURN = 22
    SELF = 23
    NEW = 24
    DELET = 25
    FUNCTION = 26
    IF = 27
    THEN = 28
    ELSEIF = 29
    ELSE = 30
    SWITCH = 31
    CASE = 32
    FOR = 33
    WHILE = 34
    DO = 35
    UNTIL = 36
    CONTINUE = 37
    BREAK = 38
    IN = 39
    NIL = 40
    NOT = 41
    END = 42
    AND = 43
    OR = 44
    TRUE = 45
    FALSE = 46
    RETURN = 47
    SELF = 48
    NEW = 49
    DELETE = 50
    FUNCTION = 51
    LBRACK = 52
    RBRACK = 53
    LPAREN = 54
    RPAREN = 55
    PLUS = 56
    INCR = 57
    DECR = 58
    MINUS = 59
    MULT = 60
    DIV = 61
    MOD = 62
    SEMICOLON = 63
    COLON = 64
    DOT = 65
    COMMA = 66
    ASSIGN = 67
    TERN = 68
    EQ = 69
    NE = 70
    LT = 71
    LE = 72
    GT = 73
    GE = 74
    BIT_AND = 75
    BIT_OR = 76
    BIT_XOR = 77
    BIT_NOT = 78
    STRING = 79
    LCURLY = 80
    RCURLY = 81



    def __init__(self, t, text, lineno, column):
        self.t = t
        self.text = text
        self.lineno = lineno
        self.column = column

class Tokenizer:
    tokens = []
    reserved_words = {
            'if': Token.IF,
            'then': Token.THEN,
            'elseif': Token.ELSEIF,
            'else': Token.ELSE,
            'switch': Token.SWITCH,
            'case': Token.CASE,
            'for': Token.FOR,
            'while': Token.WHILE,
            'do': Token.DO,
            'until': Token.UNTIL,
            'continue': Token.CONTINUE,
            'break': Token.BREAK,
            'in': Token.IN,
            'nil': Token.NIL,
            'not': Token.NOT,
            'end': Token.END,
            'and': Token.AND,
            'or': Token.OR,
            'true': Token.TRUE,
            'false': Token.FALSE,
            'return': Token.RETURN,
            'self': Token.SELF,
            'new': Token.NEW,
            'delete': Token.DELETE,
            'function': Token.FUNCTION
            }
    operators = {
            '[': Token.LBRACK,
            ']': Token.RBRACK,
            '(': Token.LPAREN,
            ')': Token.RPAREN,
            '{': Token.LCURLY,
            '}': Token.RCURLY,
            '+': Token.PLUS,
            '++': Token.INCR,
            '--': Token.DECR,
            '-': Token.MINUS,
            '*': Token.MULT,
            '/': Token.DIV,
            '%': Token.MOD,
            ';': Token.SEMICOLON,
            ':': Token.COLON,
            '.': Token.DOT,
            ',': Token.COMMA,
            '=': Token.ASSIGN,
            '?': Token.TERN,
            '==': Token.EQ,
            '!=': Token.NE,
            '<': Token.LT,
            '<=': Token.LE,
            '>': Token.GT,
            '>=': Token.GE,
            '&': Token.BIT_AND,
            '|': Token.BIT_OR,
            '^': Token.BIT_XOR,
            "~": Token.BIT_NOT
            }
    binary_operators = [
            Token.PLUS,
            Token.MINUS,
            Token.MULT,
            Token.DIV,
            Token.MOD,
            Token.EQ,
            Token.NE,
            Token.LT,
            Token.LE,
            Token.GT,
            Token.GE,
            Token.BIT_AND,
            Token.BIT_OR,
            Token.BIT_XOR
            ]
    prefix_operators = [
            Token.DECR,
            Token.INCR,
            Token.NOT,
            Token.BIT_NOT,
            Token.NEW
            ]
    postfix_operators = [
            Token.INCR,
            Token.DECR
            ]

    def __init__(self, filename):
        self.filename = filename
        self.current_line = ""
        self.lineno = 1
        self.column = -1
        self.tokenized = False

    def tokenize(self):
        with open(self.filename) as file:
            for self.current_line in file:
                self.tokenize_line()
                self.column = -1
        self.tokenized = True


    def tokenize_line(self):
        c = self.get_char()
        while c is not None:
            if c in ' \t\r\n':
                c = self.get_char()
                continue
            elif c == '/' and peak_char() == '/':
                break # comment, ignore rest of line
            elif c.isdigit(): # this is a number
                self.tokenize_number()
            elif c.isalpha(): #identifier
                self.tokenize_id()
            elif c == '\'' or c == '\"':
                self.tokenize_str()
            elif c in self.operators or (c == '!' and peak_token() == '='):
                self.tokenize_op()
            else:
                print "Error " + repr(self.lineno) + ":" + repr(self.column) + ": Unexpected Token " + int(c)
                exit()
            c = self.get_char()

        self.lineno += 1

    def tokenize_number(self):
        column = self.column
        is_decimal = False
        c = self.get_current_char()
        number = ''
        while c.isdigit() or (is_decimal is False and c == '.'):
            number += c
            c = self.get_char()

        self.tokens.append(Token(Token.NUMBER, number, self.lineno, column))

        if c is not None:
            self.unget_char()

    def tokenize_id(self):
        starting = False
        column = self.column
        c = self.get_current_char()
        identifier = ''
        while (not starting or c.isalpha()) and (c.isalnum() or c == '_' or c == '.'):
            identifier += c
            if (c == '.'):
                starting = True
            c = self.get_char()

        # Check if this is a reserved word
        rword = self.reserved_words.get(identifier)
        if rword is not None:
            self.tokens.append(Token(rword, identifier, self.lineno, column))
        else:
            self.tokens.append(Token(Token.IDENTIFIER, identifier, self.lineno, column))

        if c is not None:
            self.unget_char()

    def tokenize_op(self):
        column = self.column
        op = ""
        c = self.get_current_char()
        while op+c in self.operators:
            op += c
            c = self.get_char()

        token = self.operators[op]
        self.tokens.append(Token(token, op, self.lineno, column))

        if (c is not None):
            self.unget_char()

    def tokenize_str(self):
        column = self.column
        matched = False
        string = self.get_current_char()
        c = self.get_char()
        while c != None and (c != string[0] or (len(string) > 1 and string[-1] == '\\')):
            string += c
            c = self.get_char()

        if c != string[0]:
            print "Error " + repr(self.lineno) + ":" + repr(column) + ": Unmatched string character" + int(c)
            exit()
        string += c

        self.tokens.append(Token(Token.STRING, string, self.lineno, column))

    def get_current_char(self):
        return self.current_line[self.column]

    def get_char(self):
        if self.column+1 < len(self.current_line):
            self.column += 1
            return self.current_line[self.column]
        else:
            return None

    def unget_char(self):
        self.column = self.column-1

    def peak_char(self):
        if self.column+1 < len(self.current_line):
            return self.current_line[self.column+1]
        else:
            return None

