import sys
from parser import parser

def debug():
    for linha in sys.stdin:
        parser.success = True
        parser.parse(linha)
        if parser.success:
            print("Frase válida: ", linha)
        else:
            print("Frase inválida... Corrija e tente novamente!")

def codeGenerated():
    program = sys.stdin.read()
    code = parser.parse(program)

    print(code)

    for line in code:
        print(line, end='')

codeGenerated()