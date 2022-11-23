# main creates a REPL in which we can input source code via .txt file. It calls the parser
# which calls the lexer to tokenize the text. The parser then scans it.
from parser import *
import sys

if __name__ == '__main__':
    lexer = EneLexer()
    parser = EneParser()
    env = {}

    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        text = str(f.read())
        try:
            tree = parser.parse(lexer.tokenize(text))
        except:
            print("Program terminated")
    else:
        print('Please call the program following this format:')
        print('python3 main.py <name>.txt')