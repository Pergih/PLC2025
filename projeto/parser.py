import ply.yacc as yacc 
from lexer import lexer,tokens
from functools import reduce



symbol_table = {'global': {}}
current_scope = 'global'

next_global = 0
next_local = 0

label_counter = 0
function_code = []

precedence = (
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION'),
    ('left', 'DIV', 'MOD'),
    ('left', 'EQ', 'NEQ', 'LTE','LT','GT','GTE'),
    ('left', 'OR', 'AND'),
)

def p_program_start(t):
	'program : header SEMICOLON block DOT'
	global next_global
	
	t[0] = [f'pushn {next_global}\n', 'start\n'] + t[3] + ['stop\n'] + function_code
    

def p_header(t):
	'header : PROGRAM IDENTIFIER'
	t[0] = []
	
def p_block(t):
	'block : func_section var_section statement_section'
	t[0] = t[2]+t[3]
	
	
def p_var_section_main(t):
	'var_section : VAR var_list'
	t[0] = t[2]
		
def p_var_section_emp(t):
	'var_section : '
	t[0] = []

def p_var_list_main(t):
	'var_list : var_decl var_list'
	t[0] = t[1]+t[2]

def p_var_list_emp(t):
	'var_list : var_decl'
	t[0] = t[1]
	

def p_var_decl(t):
    'var_decl : iden_list COLON type SEMICOLON'
    global next_global

    identifiers = t[1]
    typ = t[3]
    for name in identifiers:
        if typ['kind'] == 'array':
            low  = typ['low']
            high = typ['high']
            size = high - low + 1

            symbol_table['global'][name] = {
                'kind': 'array',
                'base': next_global,
                'low': low,
                'high': high,
                'size': size,
                'type': typ['type']
            }

            next_global += size
        elif typ['kind'] == 'string':
            symbol_table['global'][name] = {
                'kind': 'string',
                'addr': next_global,
                'type': 'string'
            }
            next_global += 1

        else:
            symbol_table['global'][name] = {
                'kind': 'var',
                'addr': next_global,
                'type': typ['type']
            }
            next_global += 1

    t[0] = []
     
def p_iden_list_main(t):
    'iden_list : IDENTIFIER COMMA iden_list'
    t[0] = [t[1]]+t[3]

def p_iden_list_emp(t):
    'iden_list : IDENTIFIER'
    t[0]=[t[1]]

def p_type(t):
    '''type : scalar_type
            | array_type'''
    t[0] = t[1]

def p_scalar_type(t):
    '''scalar_type : TINTEGER
                   | TREAL
                   | TBOOLEAN
                   | TCHAR'''
    t[0] = {'kind': 'scalar', 'type': t[1].lower()}

def p_array_type(t):
    'array_type : ARRAY LBRACKET range RBRACKET OF scalar_type'
    low, high = t[3]
    t[0] = {'kind':'array', 'low':low, 'high':high, 'type': t[6]}

def p_array_type_string(t):
    'array_type : TSTRING'
    t[0] = {
        'kind': 'string',
        'type': 'string'
    }

def p_range(t):
    'range : INTEGER DOT DOT INTEGER'
    t[0] = (int(t[1]), int(t[4]))

def p_func_section_main(t):
	'func_section : func_decl SEMICOLON func_section'
	t[0] = []
	

def p_func_section_emp(t):
	'func_section : '
	t[0] = []

def p_func_decl(t):
	'func_decl : FuncHeader SEMICOLON block'
	global current_scope, function_code

	function_code += t[1] + t[3] + ['return\n']
	current_scope = 'global'
	t[0] = [] 

def p_func_head1(t):
    'FuncHeader : FUNCTION IDENTIFIER COLON type'
    global current_scope, next_local
    fname = t[2]
    symbol_table['global'][fname] = {'type': t[4]}
    current_scope = fname
    symbol_table[fname] = {}
    next_local = 0
    t[0] = [f'{fname}:\n', 'nop\n']

def p_func_head2(t):
    'FuncHeader : FUNCTION IDENTIFIER LPAREN param_list RPAREN COLON type'
    global current_scope, next_local
    fname = t[2]
    params = t[4]
    symbol_table['global'][fname] = {'type': t[7], 'nparams': len(params)}
    current_scope = fname
    symbol_table[fname] = {}
    next_local = 0

    params = [(fname,t[7])]+params
    n = len(params)
    for i, (pname, ptype) in enumerate(params):
        print('JHSDH: ', pname, ptype)
        symbol_table[fname][pname] = {'addr': -(n - i), 'type': ptype['type'], 'kind': ptype['kind']}
    t[0] = [f'{fname}:\n', 'nop\n']

def p_param_list1(t):
	'param_list : param COMMA param_list'
	t[0] = t[1] + t[3]

def p_param_list2(t):
    'param_list : param'
    t[0] = t[1]

def p_param(t):
	'param : IDENTIFIER COLON type'
	t[0] = [(t[1], t[3])]

# ERROR ------------

def p_error(t):
    if t:
        print(f"Syntax error at {t.value}. Cry about it.")
    else:
        print("Syntax error at EOF")

# For StatementSection 

def p_statement_section(t):
    'statement_section : BEGIN stmt_seq END'
    t[0] = t[2] 

# For StmtSeq

def p_stmt_seq_list(t):
    'stmt_seq : stmt SEMICOLON stmt_seq'
    t[0] = (t[1] or []) + (t[3] or [])

def p_stmt_seq_single(t):
    'stmt_seq : stmt SEMICOLON'
    t[0] = t[1]

# For Statments

def p_stmtAssignment(t):
    r"stmt : Assignment"
    t[0] = t[1]['code']



def p_stmtContinuation(t):
    r"stmt : statement_section"
    t[0] = t[1]


def p_stmtIfStmt(t):
    r"stmt : IfStmt"
    t[0] = t[1]


def p_stmtWhileStmt(t):
    r"stmt : WhileStmt"
    t[0] = t[1]

def p_stmtRepeatStmt(t):
    r"stmt : RepeatStmt"  
    t[0] = t[1]

def p_stmtForStmt(t):
    r"stmt : ForStmt"
    t[0] = t[1]


def p_stmt_func_call(t):
    'stmt : FuncCall'
    t[0] = t[1]

def p_stmtWriteln(t):
    'stmt : Writeln'
    t[0] = t[1]

def p_stmtReadln(t):
    'stmt : Readln'
    t[0] = t[1]


#For Assignment

def p_assignment(t):
    'Assignment : IDENTIFIER ASSIGNMENT expression'
    var = t[1]

    if current_scope != 'global' and var in symbol_table[current_scope]:
        addr = symbol_table[current_scope][var]['addr']
        code = t[3] + [f'storel {addr}\n']
    else:
        addr = symbol_table['global'][var]['addr']
        code = t[3] + [f'storeg {addr}\n']

    t[0] = {
        'var': var,
        'code': code
    }

def p_assignment_array(t):
    'Assignment : IDENTIFIER LBRACKET expression RBRACKET ASSIGNMENT expression'

    if current_scope != 'global' and t[1] in symbol_table[current_scope]:
        arr = symbol_table[current_scope][t[1]]
        base_code = ['pushfp\n', f'pushi {arr["base"]}\n', 'padd\n']
    else:
        arr = symbol_table['global'][t[1]]
        base_code = ['pushgp\n', f'pushi {arr["base"]}\n', 'padd\n']

    low = arr['low']

    t[0] = {
        'code': (
            base_code +
            t[3] +
            [f'pushi {low}\n', 'sub\n'] +
            t[6] +
            ['storen\n']
        )
    }

# For Expressions

def p_expression(t):
    r"expression : expression LogicOp ExpressionM"
    t[0] = t[1] + t[3] + [f'add\n'] + t[2] 

def p_expressionWExpM(t):
    r"expression : ExpressionM"
    t[0] = t[1]

def p_expressionMWExpS(t):
    r"ExpressionM : ExpressionS"
    t[0] = t[1]

def p_expressionMWExpM(t):
    r"ExpressionM : ExpressionM Op ExpressionS"
    t[0] = t[1] + t[3] + t[2]
    
def p_expressionSWouExpS(t):
    r"ExpressionS : Element"
    t[0] = t[1]['code'] 

def p_expressionSWExpS(t):
    r"ExpressionS : ExpressionS PriOp Element"
    t[0] = t[1] + t[3]['code'] + t[2]

# For Elements

def p_elementId(t):
    r"Element : IDENTIFIER"
    if current_scope != 'global' and t[1] in  symbol_table[current_scope]:
        addr = symbol_table[current_scope][t[1]]['addr']
        type = symbol_table[current_scope][t[1]]['type']
        code = [f'pushl {addr}\n']
    else:
        addr = symbol_table['global'][t[1]]['addr']
        type = symbol_table['global'][t[1]]['type']
        code = [f'pushg {addr}\n']
        
    name = t[1]
    t[0] = {
        'value': name,
        'type': type,
        'code': code
    }
    
def p_elementReal(t):
    r"Element : REAL"
    type = 'real'
    code = [f"pushf {t[1]}\n"]
    t[0] = {
        'type' : type,
        'code': code
    }

def p_elementBoolean(t):
    r"Element : BOOLEAN"

    type = 'boolean'
    code = [f"pushi {1 if t[1]=='true' else 0}\n"]
    t[0] = {
        'type' : type,
        'code': code
    }

def p_elementInt(t):
    r"Element : INTEGER"
    type = 'integer'
    code = [f"pushi {t[1]}\n"]
    t[0] = {
        'type' : type,
        'code': code
    }

def p_elementString(t):
    r"Element : STRING"

    t[0] = {
        'type': 'string',
        'code': [f'pushs "{t[1]}"\n'],
        'value': t[1]
    }
    
def p_elementChar(t):
    'Element : CHAR'

    type = 'char'
    t[0] = {
        'code': [f'pushi {ord(t[1][1:-1])}\n'],
        'type': type
    }


def p_elementExpression(t):
    r"Element : LPAREN expression RPAREN"
    code = t[2]
    type = 'expression'
    t[0] = {
        'type' : type,
        'code': code
    }




def p_elementFunction(t):
    r"Element : InlineFuncCall"
    type = 'inLineFuncCall'
    code = t[1]['code']
    name = t[1]['value']
    t[0] = {
        'value': name,
        'type' : type,
        'code': code
    }

def p_elementArray(t):
    r"Element : ArrayAccess"
    type = 'arrayAcess'
    code = t[1]['code']
    name = t[1]['value']
    t[0] = {
        'value': name,
        'type' : type,
        'code': code
    }


# For Arrays

def p_arrayAccess(t):
    'ArrayAccess : IDENTIFIER LBRACKET expression RBRACKET'
    name = t[1]

    if current_scope != 'global' and name in symbol_table[current_scope]:
        sym = symbol_table[current_scope][name]
        is_local = True
    else:
        sym = symbol_table['global'][name]
        is_local = False

    # STRING
    if sym.get('kind') == 'string':
        if is_local:
            ptr_code = [f'pushl {sym["addr"]}\n']
        else:
            ptr_code = [f'pushg {sym["addr"]}\n']

        code = (
            # string pointer (m)
            ptr_code +
            # índice (n)
            t[3]+['pushi -1\n', 'add\n']+
            ['charat\n']
        )

        t[0] = {
            'value': name,
            'code': code,
            'type': 'char'
        }
        return

    # ARRAY
    base_code = []
    if is_local:
        base_code = ['pushfp\n', f'pushi {sym["base"]}\n', 'padd\n']
    else:
        base_code = ['pushgp\n', f'pushi {sym["base"]}\n', 'padd\n']

    low = sym['low']

    code = (
        base_code +
        t[3] +
        [f'pushi {low}\n', 'sub\n'] +
        ['loadn\n']
    )

    t[0] = {
        'value': name,
        'code': code,
        'type': sym['type']
    }
    

# For InLineFuncCall

def p_inLineFuncCall(t):
    r"InlineFuncCall : IDENTIFIER LPAREN param_expr_list RPAREN"

    n_params = symbol_table['global'][t[1]]['nparams']
    code = (
        ['pushi 0\n'] + 
        t[3] + 
        [f'pusha {t[1]}\n', 'call\n', f'pop {n_params}\n']
    )

    name = t[1]
    t[0] =  {
        'value': name,
        'code': code
    }
   

# For Operations

def p_logicOpAnd(t):
    r"LogicOp : AND"
    t[0] = [f'pushi 2\n', "equal\n"]
    

def p_logicOpOr(t):
    r"LogicOp : OR"
    t[0] = ["pushi 0\n", "equal\n", "not\n"]
    
# For Op

def p_opPlus(t):
    r"Op : PLUS"
    t[0] = ["add\n"]


def p_opMinus(t):
    r"Op : MINUS"
    t[0] = ["sub\n"]
    
    
def p_opDiv(t):
    r"Op : DIV"
    t[0] = ["div\n"]
    
def p_opEq(t):
    r"Op : EQ"
    t[0] = ["equal\n"]
    
def p_opNeq(t):
    r"Op : NEQ"
    t[0] = ["equal\n", "not\n"]
    
def p_opMod(t):
    r"Op : MOD"
    t[0] = ["mod\n"]
    
def p_opLT(t):
    r"Op : LT"
    t[0] = ["inf\n"]
    
def p_opLTE(t):
    r"Op : LTE"
    t[0] = ["infeq\n"]
    
def p_opGT(t):
    r"Op : GT"
    t[0] = ["sup\n"]
    
def p_opGTE(t):
    r"Op : GTE"
    t[0] = ["supeq\n"]
    
# For PriOp

def p_priOpTimes(t):
    r"PriOp : TIMES"
    t[0] = ["MUL\n"]

def p_priOpDivision(t):
    r"PriOp : DIVISION" 
    t[0] = ["div\n"]
    
# For FuncCall

def p_funcCall(t):
    r"FuncCall : IDENTIFIER LPAREN param_expr_list RPAREN"
    n = len(t[3]) # Numero de vezes para dar pop
    t[0] = t[3] + [f"pusha {t[1]}\n", 'call\n'] + ([f"pop {n}\n"])
    
# For param_expr_list

def p_param_expr_list(t):
    r"param_expr_list : param_expr_list COMMA ParamExpr"
    t[0] = t[1] + t[3]
    
def p_param_expr_listParamExpr(t):
    r"param_expr_list : ParamExpr"
    t[0] = t[1]
    
# For ParamExpr

def p_ParamExpr(t):
    r"ParamExpr : expression"
    t[0] = t[1]
    
# For IfStmt

def p_IfStmtElse(t):
    r"IfStmt : IF expression THEN stmt ELSE stmt"
    global label_counter
    else_label = f"else{label_counter}"
    else_label_nop = [f"else{label_counter}: NOP\n"]
    if_end_label = f"ifEnd{label_counter}"
    if_end_label_nop = [f"ifEnd{label_counter}: NOP\n"]
    label_counter = label_counter + 1
    t[0] = t[2] + [f"jz {else_label}\n"] + t[4] + [f"jump {if_end_label}\n"] + ["\n"] + else_label_nop + t[6] + ["\n"] + if_end_label_nop

def p_IfStmt(t):
    r"IfStmt : IF expression THEN stmt"
    global label_counter
    label = f"else{label_counter}"
    label_nop = [f"else{label_counter}: NOP\n"]
    label_counter = label_counter + 1
    t[0] = t[2] + [f"jz {label}\n"] + t[4] + ["\n"] + label_nop

# For WhileStmt

def p_WhileStmt(t):
    r"WhileStmt : WHILE expression DO stmt"
    global label_counter
    while_label = f"while{label_counter}"
    while_label_nop = [f"while{label_counter}: NOP\n"]
    end_while_label = f"endWhile{label_counter}"
    end_while_label_nop = [f"endWhile{label_counter}: NOP\n"]
    label_counter = label_counter + 1
    t[0] = ["\n"] + while_label_nop + t[2] + [f"jz {end_while_label}\n"] + t[4] + [f"jump {while_label}\n"] + ["\n"] + end_while_label_nop


# For RepeatStmt

def p_RepeatStmt(t):
    r"RepeatStmt : REPEAT stmt UNTIL expression"
    global label_counter
    repeat_label = f"repeat{label_counter}"
    repeat_label_nop = [f"repeat{label_counter}: NOP\n"]
    label_counter = label_counter + 1
    t[0] = ["\n"] + repeat_label_nop + t[2] + t[4] + [f"jz {repeat_label}"] + ["\n"]
    
    
# For ForStmt

def p_ForStmt(t):
    r"ForStmt : FOR Assignment TO expression DO stmt"
    global label_counter, symbol_table
    assign = t[2]
    var = assign['var']
    init_code = assign['code']
    var_addr = symbol_table['global'][var]['addr']
    start_label = f"for{label_counter}"
    end_label   = f"endFor{label_counter}"
    label_counter = label_counter + 1
    t[0] = (
            init_code
            + [f"{start_label}: NOP\n"]

            + [f"pushg {var_addr}\n"]
            + t[4]
            + ["infeq\n"]
            + [f"jz {end_label}\n"]

            + t[6]

            + [f"pushg {var_addr}\n"]
            + ["pushi 1\n"]
            + ["add\n"]
            + [f"storeg {var_addr}\n"]

            + [f"jump {start_label}\n"]
            + [f"{end_label}: NOP\n"]
        )
    
  
def p_ForStmtDownTo(t):
    r"ForStmt : FOR Assignment DOWNTO expression DO stmt"
    global label_counter

    assign = t[2]
    var = assign['var']
    init_code = assign['code']
    var_addr = symbol_table['global'][var]['addr']

    start_label = f"for{label_counter}"
    end_label   = f"endFor{label_counter}"
    label_counter += 1

    t[0] = (
        init_code
        + [f"{start_label}: NOP\n"]

        + [f"pushg {var_addr}\n"]
        + t[4]
        + ["supeq\n"]
        + [f"jz {end_label}\n"]

        + t[6]

        + [f"pushg {var_addr}\n"]
        + ["pushi 1\n"]
        + ["sub\n"]
        + [f"storeg {var_addr}\n"]

        + [f"jump {start_label}\n"]
        + [f"{end_label}: NOP\n"]
    )

# For Writln

def p_Writeln(t):
    'Writeln : WRITELN LPAREN ElementList RPAREN'
    t[0] = t[3]

def p_ElementList(t): 
    'ElementList : Element COMMA ElementList'
    type = t[1]['type']
    if type == 'integer' or type == 'expression' or type == 'length' :
        wrt = [f"writei\n"]
    elif type == 'real':
        wrt = [f"writef\n"]
    elif type == 'string':
        wrt = [f"writes\n"]
    elif type == 'identifier' or type == 'inLineFuncCall' or type == 'arrayAcess':
        name = t[1]['value']
        type2 = symbol_table['global'][name]['type']
        if type2 == 'treal':
            wrt = [f"writef\n"]
        elif type2 == 'tinteger':
            wrt = [f"writei\n"]
        else:
            wrt = [f"writes\n"]
    else:
        raise Exception("Error: Tipo de parametro desconhecido")
    t[0] = t[1]['code'] + wrt + t[3] + ['writeln\n']

def p_ElementListSingle(t):
    'ElementList : Element '
    type = t[1]['type']

    if type == 'integer' or type == 'expression' or type == 'length' :
        wrt = [f"writei\n"]
    elif type == 'real':
        wrt = [f"writef\n"]
    elif type == 'string':
        wrt = [f"writes\n"]
    elif type == 'identifier' or type == 'inLineFuncCall' or type == 'arrayAcess':
        name = t[1]['value']
        type2 = symbol_table['global'][name]['type']
        if type2 == 'real':
            wrt = [f"writef\n"]
        elif type2 == 'integer':
            wrt = [f"writei\n"]
        else:
            wrt = [f"writes\n"]
    else:
        raise Exception("Error: Tipo do parametro desconhecido")
    
    t[0] = t[1]['code'] + wrt

# For Readln

def p_Readln(t):
    'Readln : READLN LPAREN ReadTargetList RPAREN'
    t[0] = t[3]

def p_ReadTargetList_multiple(t):
    'ReadTargetList : ReadTarget COMMA ReadTargetList'
    t[0] = t[1] + t[3]

def p_ReadTargetList_single(t):
    'ReadTargetList : ReadTarget'
    t[0] = t[1]

def p_ReadTarget_var(t):
    'ReadTarget : IDENTIFIER'
    name = t[1]
    sym = symbol_table[current_scope].get(name, symbol_table['global'].get(name))
    
    if sym['kind'] == 'string':
        code = ['read\n', f'storeg {sym["addr"]}\n']
    else:
        if sym['type'] == 'real':
            code = ['read\n', 'atof\n', f'storeg {sym["addr"]}\n']
        elif sym['type'] == 'integer':
            code = ['read\n', 'atoi\n', f'storeg {sym["addr"]}\n']
        else:
            code = ['read\n', f'storeg {sym["addr"]}\n']
    
    t[0] = code

def p_ReadTarget_array(t):
    'ReadTarget : IDENTIFIER LBRACKET expression RBRACKET'
    name = t[1]
    index_code = t[3]  
    sym = symbol_table[current_scope].get(name, symbol_table['global'].get(name))
    
    if sym['kind'] not in ['array', 'string']:
        raise Exception(f"{name} não é array ou string")

    if current_scope != 'global' and name in symbol_table[current_scope]:
        base_code = ['pushfp\n', f'pushi {sym.get("base", sym.get("addr"))}\n', 'padd\n']
    else:
        base_code = ['pushgp\n', f'pushi {sym.get("base", sym.get("addr"))}\n', 'padd\n']

    array_type = sym['type']['type'] if sym['kind'] == 'array' else sym['type']
    
    if array_type == 'integer':
        read_code = ['read\n', 'atoi\n']
    elif array_type == 'real':
        read_code = ['read\n', 'atof\n']
    elif array_type == 'char':
        read_code = ['read\n'] 
    elif array_type == 'string':
        read_code = ['read\n']
    else:
        raise Exception(f"Tipo não suportado para leitura em array: {array_type}")

    low = sym['low']
    code = base_code + index_code + [f'pushi {low}\n', 'sub\n']+ read_code + ['storen\n']
    t[0] = code


# For Length

def p_Length(t):
    'Element : LENGTH LPAREN expression RPAREN'
    t[0] = {
        'type': 'integer',
        'code': t[3] + ['strlen\n']
    }

parser = yacc.yacc(debug=True)