# Exemplo das expressões aritméticas

import ply.lex as lex

tokens = (
    'INT',
    'REAL',
    'ID',
    'ATRIB',
    'SOMA',
    'MUL',
)

t_SOMA = r'\+'
t_MUL = r'\*'
t_ATRIB = r'='

def t_ID(t):
    r'[A-Za-z_]\w*'
        
    return t

def t_REAL(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)

    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)

    return t


t_ignore = ' \t\n'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# -------------------------------------------

# data = '''
# 3 + 4 * 10
#   + -20 *2
# F = 32 + 1.8 * C
# '''

# lexer.input(data)

# for tok in lexer:
#     print(tok)