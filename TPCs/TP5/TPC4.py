import ply.lex as lex
import sys
import json
import datetime as datetime

def calcular_troco(valor):
    troco = round(valor)
    moedas = {
        "2e": 0,
        "1e": 0,
        "50c": 0,
        "20c": 0,
        "10c": 0,
        "5c": 0,
        "2c": 0,
        "1c": 0
    }
    valores = [
        (200, "2e"),
        (100, "1e"),
        (50, "50c"),
        (20, "20c"),
        (10, "10c"),
        (5, "5c"),
        (2, "2c"),
        (1, "1c")
    ]

    for v, nome in valores:
        moedas[nome] = troco // v
        troco %= v

    return moedas

def print_saldo(n, s = "SALDO = "):
    if n%100 == 0:
        print(f'{s}{int(n//100)}e')
    elif n//100 == 0:
        print(f'{s}{int(n%100)}c')
    else:
        print(f'{s}{int(n//100)}e{int(n%100)}c')
    return
states = (
    ('MOEDA','exclusive'),
    ('SELECIONAR','exclusive'),
    ('ADICIONAR','exclusive'),
)

tokens = (
    'MOEDA', # Estado
    'EUROS',
    'CENTIMOS',
    'DOT',
    
    'SELECIONAR', # Estado
    'CODIGO',
    
    'ADICIONAR', # Estado
    # 'CODIGO',
    
    # INICIAL
    'SALDO',
    'LISTAR',
    'SAIR',
)

#####
# MOEDA QUERY
#####

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('MOEDA')

def t_MOEDA_EUROS(t):
    r'(2e|1e)'
    t.value = int(t.value[:-1]) * 100
    t.lexer.saldo += t.value
    return t

def t_MOEDA_CENTIMOS(t):
    r'(50c|20c|10c|5c)'
    t.value = int(t.value[:-1])
    t.lexer.saldo += t.value
    return t

def t_MOEDA_DOT(t):
    r'\.$'
    print_saldo(t.lexer.saldo)
    t.lexer.begin('INITIAL')
    return t

t_MOEDA_ignore = ' \t,\n'

def t_MOEDA_error(t):
    print(f"Erro léxico no estado MOEDA: {t.value[0]!r}")
    t.lexer.skip(1)


#####
# SELECIONAR QUERY
#####

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('SELECIONAR')
    return t

def t_SELECIONAR_CODIGO(t):
    r'[A-Z]\d+'
    for i in range(len(t.lexer.stock)):
        if t.lexer.stock[i]['cod'] == t.value:
            prod = t.lexer.stock[i]
    if prod['quant'] > 0 and prod['preco'] <= t.lexer.saldo:
        print(f"Pode retirar o produto dispensado \"{prod['nome']}\"")
        prod['quant'] -= 1
        
        t.lexer.saldo -= prod['preco'] * 100
        print_saldo(t.lexer.saldo)
    elif prod['preco'] > t.lexer.saldo:
        print("Saldo insufuciente para satisfazer o seu pedido")
        print_saldo(t.lexer.saldo)
        print_saldo(prod['preco'], "Pedido = ")
    else:
        print("Produto sem stock")
    t.lexer.begin('INITIAL')
    return t

t_SELECIONAR_ignore = ' \t\n'

def t_SELECIONAR_error(t):
    print(f"Erro léxico no estado SELECIONAR: {t.value[0]!r}")
    t.lexer.skip(1)
    
#####
# ADICIONAR QUERY
#####

def t_ADICIONAR(t):
    r'ADICIONAR'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('ADICIONAR')
    return t

def t_ADICIONAR_CODIGO(t):
    r'[A-Z]\d+'
    for i in range(len(t.lexer.stock)):
        if t.lexer.stock[i]['cod'] == t.value:
            prod = t.lexer.stock[i]
    print(f"Produto adicionado \"{prod['nome']}\"")
    prod['quant'] += 1
        
    t.lexer.begin('INITIAL')
    return t

t_ADICIONAR_ignore = ' \t\n'

def t_ADICIONAR_error(t):
    print(f"Erro léxico no estado ADICIONAR: {t.value[0]!r}")
    t.lexer.skip(1)

#####
# INITIAL
#####

def t_LISTAR(t):
    r'LISTAR'
    
    print("cod | nome                      | quantidade | preço")
    print("----------------------------------------------------")
    for item in stock:
        print(f"{item['cod']:3} | {item['nome']:<25} | {item['quant']:10} | {item['preco']:.2f}")
    return t

def t_SAIR(t):
    r'SAIR'
    saldo = t.lexer.saldo
    if saldo > 0:
        moedas = calcular_troco(saldo)
        partes = []
        for m, qtd in moedas.items():
            if qtd > 0:
                partes.append(f"{qtd}x {m}")
        print("Pode retirar o troco: " + ", ".join(partes) + ".")
    else:
        print("Sem troco a devolver.")
        
    print("Até à próxima")
    with open("stock.json", "w", encoding="utf-8") as f:
        json.dump(t.lexer.stock, f, ensure_ascii=False, indent=4)
    sys.exit(0)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


try:
    with open("stock.json", "r", encoding="utf-8") as f:
        stock = json.load(f)
except FileNotFoundError:
    # default
    stock = [
        {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
    ]

lexer = lex.lex()

lexer.stock = stock
print(f"{datetime.datetime.now()}, Stock carregado, Estado atualizado.")
lexer.saldo = 0
print("Bom dia. Estou disponível para atender o seu pedido.")

for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(str(tok))