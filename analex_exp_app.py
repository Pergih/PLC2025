import analex_exp as alex
import sys

for linha in sys.stdin:
    alex.lexer.input(linha)
    for tok in alex.lexer:
        print(tok)