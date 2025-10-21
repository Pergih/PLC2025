import sys
import re

def tokenize(input_string):
    reconhecidos = []
    linha = 1
    mo = re.finditer(r'(?P<SELECT>^SELECT)|(?P<WHERE>WHERE)|(?P<NEWLINE>\n)|(?P<VARIABLE>\?\w+)|(?P<STRING>\w*\:\w+)|(?P<SKIP>[ \t])|(?P<PA>{)|(?P<PF>})|(?P<POINT>\.$)|(?P<ERRO>.)', input_string)
    for m in mo:
        dic = m.groupdict()
        if dic['SELECT']:
            t = ("SELECT", dic['SELECT'], linha, m.span())
    
        elif dic['WHERE']:
            t = ("WHERE", dic['WHERE'], linha, m.span())
    
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())
    
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
    
        elif dic['VARIABLE']:
            t = ("VARIABLE", dic['VARIABLE'], linha, m.span())
    
        elif dic['STRING']:
            t = ("STRING", dic['STRING'], linha, m.span())
        
        elif dic['PA']:
            t = ("PA", dic['PA'], linha, m.span())
        
        elif dic['PF']:
            t = ("PF", dic['PF'], linha, m.span())
        
        elif dic['POINT']:
            t = ("POINT", dic['POINT'], linha, m.span())
        
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())
    
        else:
            t = ("UNKNOWN", m.group(), linha, m.span())
        if not dic['SKIP'] and t[0] != 'UNKNOWN': reconhecidos.append(t)
    return reconhecidos

for linha in sys.stdin:
    for tok in tokenize(linha):
        print(tok)    
