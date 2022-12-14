# Gets source code, groups characters into tokens to be scanned by the parser.
from sly import Lexer

class EneLexer(Lexer):

    # Keywords
    tokens = {PROGRAM, MAIN, FUNC, ID, INT, FLOAT, CHAR, STRING, DATAFRAME,
              CTEINT, CTEFLOAT, CTECHAR, CTESTRING, IF, ELSE, AND, OR, PRINT,
              WRITE, WHILE, DO, FOR, RETURN, LOAD, MEDIAN, CORRELATE}

    # Ignore whitespace
    ignore = '\t'

    # Operators and delimiters
    literals = {';',',',':','{','}','=','!','(',')','+','-','*','/','<','>','[',']'}

    # Definitions
    PROGRAM = r'program'
    MAIN = r'main'
    FUNC = r'func'
    INT = r'int'
    FLOAT = r'float'
    CHAR = r'char'
    STRING = r'string'
    DATAFRAME = r'dataframe'
    IF = r'if'
    ELSE = r'else'
    AND = r'and'
    OR = r'or'
    PRINT = r'print'
    WRITE = r'write'
    WHILE = r'while'
    DO = r'do'
    FOR = r'for'
    RETURN = r'return'
    LOAD = r'load'
    MEDIAN = r'median'
    CORRELATE = r'correlate'

    # Skip whitespace
    @_(r'\n')
    def newline(self,t):
        pass

    # Skip whitespace
    @_(r' ')
    def space(self,t):
        pass

    # ID starts with a letter, followed by any combination of letters and digits
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self,t):
        return t

    # Float is any whole number followed by a dot followed by a whole number
    @_(r'\d+\.\d+')
    def CTEFLOAT(self,t):
        t.value = float(t.value)
        return t

    # Int is any whole number
    @_(r'\d+')
    def CTEINT(self,t):
        t.value = t.value
        return t

    # Any single symbol surrounded by ''
    @_(r'\'.*\'')
    def CTECHAR(self, t):
        t.value = t.value
        return t

    # Anything surrounded by ""
    @_(r'\"([^""]+)\"')
    def CTESTRING(self, t):
        t.value = t.value
        return t


