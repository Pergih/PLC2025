import ply.lex as lex
import re

tokens = (
    # Assignment
	'IDENTIFIER',
	'ASSIGNMENT',
	'SEMICOLON',
	'COLON',
	'COMMA',
    'OF',

	# Main
	'PROGRAM',
	'DOT',
	
	# Blocks
	'VAR',
	'BEGIN',
	'END',
	
	# Control flow
	'IF',
	'THEN',
	'ELSE',
	'FOR',
	'WHILE',
	'REPEAT',
	'UNTIL',
	'DO',
	'TO',
	'DOWNTO',
	
	# Logic
	'AND',
	'OR',
	'NOT',
	
	# Operations
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVISION',
	'DIV',
	'MOD',
	
	# Comparations
	'EQ',
	'NEQ',
	'LT',
	'GT',
	'LTE',
	'GTE',

    # Functions
	'LPAREN',
	'RPAREN',
    'LBPAREN',
	'RBPAREN',
    'LBRACKET',
    'RBRACKET',
	'FUNCTION',

	# Types
	'REAL',
	'INTEGER',
	'STRING',
	'CHAR',
    'BOOLEAN',
    'ARRAY',
	
	# Types names
	'TREAL',
	'TINTEGER',
	'TSTRING',
	'TCHAR',
    'TBOOLEAN',
    
	# Predefined Functions
    'READLN',
    'WRITELN',
    'LENGTH'
    

)

# Regular statement rules for tokens.
t_DOT			= r"\."

t_ASSIGNMENT	= r":="
t_SEMICOLON		= r";"
t_COLON			= r":"
t_COMMA			= r","

t_PLUS			= r"\+"
t_MINUS			= r"\-"
t_TIMES			= r"\*"
t_DIVISION		= r"/"

t_EQ			= r"\="
t_NEQ			= r"\<\>"
t_LT			= r"\<"
t_GT			= r"\>"
t_LTE			= r"\<\="
t_GTE			= r"\>\="

t_LPAREN		= r"\("
t_RPAREN		= r"\)"
t_LBRACKET		= r"\["
t_RBRACKET		= r"\]"

t_REAL			= r"(\-)*[0-9]+\.[0-9]+"
t_INTEGER		= r"(\-)*[0-9]+"

# Reserved words
reserved_keywords = {
	'program':	'PROGRAM',
	'var':		'VAR',
	'begin':	'BEGIN',
	'end':		'END',
    'of':       'OF',
	
	'if':		'IF',
	'then':		'THEN',
	'else':		'ELSE',
	'for':		'FOR',
	'while':	'WHILE',
	'repeat':	'REPEAT',
	'do':		'DO',
	'to':		'TO',
	'downto':	'DOWNTO',
	'until':	'UNTIL',
	
	'and':		'AND',
	'or':		'OR',
	'not':		'NOT',
	
	'div':		'DIV',
	'mod':		'MOD',
	
	'function':	'FUNCTION',
	
	'real':		'TREAL',
	'integer':	'TINTEGER',
	'string':	'TSTRING',
    'boolean':	'TBOOLEAN',
	'char':	    'TCHAR',
    'array':	'ARRAY',
    
	'readln':   'READLN',
	'writeln':	'WRITELN',
	'length':	'LENGTH',
}    

def t_BOOLEAN(t):
    r"true|false"
    return t

def t_IDENTIFIER(t):
	r"[a-zA-Z]([a-zA-Z0-9])*"
	if t.value.lower() in reserved_keywords:
		t.type = reserved_keywords[t.value.lower()]
	return t


def t_CHAR(t):
	r"(\'([^\\\'])\')"
	return t


def t_STRING(t): 
    r"(\'([^\\\']|(\\.))*\')"
    escaped = 0 # lidar com \n dentro do string
    str = t.value[1:-1] 
    new_str = "" 
    for i in range(0, len(str)): 
        c = str[i] 
        if escaped: 
            c = "\n" if c=="n" else "\t"
            new_str += c 
            escaped = 0 
        else: 
            if c == "\\": 
                escaped = 1 
            else: 
                new_str += c 
    t.value = new_str 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t\r'

def t_error(t):
    print(f'Illegal character {t.value[0]}')
    

lexer = lex.lex()


