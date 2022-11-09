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
            print("fail")
    else:
        print('porfavor llamar el programa de esta manera:')
        print('python3 main.py nombredearchivo.txt')