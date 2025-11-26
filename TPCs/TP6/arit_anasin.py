from arit_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

# P1: Exp  --> int Exp2
# P2:        | '(' Exp ')' Exp2
# P3: Exp2 --> op Exp
# P4:        | 

def rec_Exp2():
    global prox_simb
    if prox_simb is None:
        print("Derivando por P4: Exp2 --> ")
        print("Reconheci P4: Exp2 --> ")
        return
    
    if prox_simb.type == 'OP':
        print("Derivando por P3: Exp2 --> op Exp")
        rec_term('OP')
        rec_Exp()
        print("Reconheci P3: Exp2 --> op Exp")
    elif prox_simb.type == 'PF': 
        print("Derivando por P4: Exp2 --> ")
        print("Reconheci P4: Exp2 --> ")

    else:
        parserError(prox_simb)

def rec_Exp():
    global prox_simb
    if prox_simb.type == 'INT':
        print("Derivando por P1: Exp --> int Exp2")
        rec_term('INT')
        rec_Exp2()
        print("Reconheci P1: Exp --> int Exp2")

    elif prox_simb.type == 'PA':
        print("Derivando por P2: '(' Exp ')' Exp2")
        rec_term('PA')
        rec_Exp()
        rec_term('PF')
        rec_Exp2()
        print("Reconheci P2: '(' Exp ')' Exp")
    else:
        parserError(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Exp()
    print("That's all!")
    