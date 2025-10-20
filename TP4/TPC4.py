import ply.lex as lex
import sys

states = (
    ('MOEDA','exclusive'),
    ('SELECIONAR','exclusive'),
)

tokens = (
    'CODIGO',
    'SALDO'
)

def t_CODIGO(t):
    r'A\d+'
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('')
    return t

def t_SAIR(t):
    return t

def t_LISTAR(t):
    r'LISTAR'
    print(t.lexer.stock)
    return t

def t_SALDO(t):
    r'SALDO'
    print(t.lexer.saldo)
    return t

def t_EUROS(t):
    r'\d+e'
    t.value = int(t.value[:-1]) * 100
    t.lexer.saldo += t.value
    return t 

def t_CENTIMOS(t):
    r'\d+c'
    t.value = int(t.value[:-1])
    t.lexer.saldo += t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


stock = [
 {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
]

lexer = lex.lex()
lexer.stock = stock
lexer.saldoMaq = {"2e" : 0, "1e" : 0, "50c": 0, "20c" : 0, "10c" : 0, "5c" : 0} 
lexer.saldo = 0

for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(str(tok))