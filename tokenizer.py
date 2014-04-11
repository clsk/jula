class Token:
    def __init__(self, t, text):
        self.t = t
        self.text = text

class Tokenizer:
    reserved_words = { "IF"
            }
    def __init__(self):
        self.current_line = ""
        self.lineno = 0
        self.column = 0
        self.current = ""

    def tokenize_expression():
        pass

    def tokenize_line():
        self.lineno = self.lineno + 1

    def get_char():
        self.column = self.column+1
        return self.current_line[self.column]

    def unget_char():
        self.column = self.column-1

    def peak_char():
        return self.current_line[self.column+1]

