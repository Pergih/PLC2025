import ply.lex as lex

tokens = ('PA', 'PF', 'OP', 'INT')

t_PA = r'\('
t_PF = r'\)'
t_OP = r'(\+|-|\*|/)'
t_INT = r'\d+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()


# import sys

# for linha in sys.stdin:
#     lexer.input(linha)
#     for tok in lexer:
#         print(str(tok))
