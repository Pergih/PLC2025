<div align="center">

![Logotipo da Universidade](images/um.jpeg)

# **Projeto de Processamento de Linguagens 2025**

### Construção de um Compilador para Pascal Standard

<br>

**Unidade Curricular:** Processamento de Linguagens  
**Curso:** Licenciatura em Ciências da Computação  
**Instituição:** Universidade do Minho  

</div>

<br>

<table width="100%">
<tr>
<td width="65%">

**Autores:**

A108647 — João Oliveira  
A108473 — André Pinheiro  
A108398 — Pedro Mo  

</td>

<td width="35%" align="right">

<img src="images/joao.jpg" width="90"/>  
<img src="images/andre.jpg" width="90"/>  
<img src="images/pedro.jpg" width="90"/>

</td>
</tr>
</table>

<br><br>

<div style="page-break-after: always"></div> 



### Índice



### Introdução

No âmbito da unidade curricular de Processamento de Linguagens, foi-nos solicitado a construção de um compilador de Pascal Standard que seja capaz de processar programas, incluindo declaração de variáveis, expressões aritméticas, comandos de controle de fluxo (if, while,for) e subprogramas.

### Estrutura

A estrutura deste projeto baseia-se em 3 ficheiros  **(lexer.py, parser.py e program.py)** , responsáveis pela construção do compilador. Tem-se ainda alguns ficheiros **(.txt)** que contém exemplos para testar o funcionamento do compilador construído.
#### program.py
Neste ficheiro é onde ocorre a leitura do código pascal standard, atráves da chamada da função **CodeGenerated()**. De seguida este código é enviado para o parser, que juntamente com o lexer vai transformar o código pascal em código de máquina virtual para depois ser impresso para o ecrã.
#### lexer.py

Este ficheiro é o responsável pela a análise léxica do compilador utilizando **ply.lex**, atráves do reconhecimento de padrões (expressões regulares), no código pascal inserido como input, que depois é transformado numa sequência de tokens.

Tokens existentes:
```python
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
```

#### parser.py
No presente ficheiro encontra-se a análise sintática e análise semântica do compilador. É utilizado **ply.yacc**, que pega  na sequência de tokens fornecida pelo lexer, verifica se estes seguem as regras da gramática da linguagem, e se os valores e regras da linguagem são válidos. Se todas estas verificações forem válidas,  o código pascal é transformado em código de máquina virtual segundo funções que vão de acordo com a gramática.

Gramática utilizada:

```Md
program -> header SEMICOLOM block DOT

header -> PROGRAM IDENTIFIER

block -> func_section var_section statement_section

var_section -> VAR var_list
    |

var_list -> var_decl VarList
    | var_decl

var_decl -> iden_list COLON type SEMICOLON

iden_list -> IDENTIFIER COMMA iden_list
    | IDENTIFIER

type -> scalar_type
    | array_type

scalar_type -> TINTEGER
    | TREAL
    | TBOOLEAN
    | TCHAR

ArrayType -> ARRAY LBRACKET range RBRACKET OF scalar_type
    | TSTRING

range -> INTEGER DOT DOT INTEGER

func_section -> func_decl SEMICOLON func_section
    |

func_decl -> FuncHeader SEMICOLON block

FuncHeader -> FUNCTION IDENTIFIER COLON type
    | FUNCTION IDENTIFIER LPAREN param_list RPAREN COLON type

param_list -> param COMMA param_list
    | param

param -> IDENTIFIER COLON type


statement_section -> BEGIN stmt_seq END

stmt_seq -> stmt SEMICOLON stmt_seq
    | stmt SEMICOLON

stmt -> Assignment
    | statement_section
    | IfStmt
    | WhileStmt
    | RepeatStmt
    | ForStmt
    | FuncCall
    | Writeln
    | Readln
    
Assignment -> IDENTIFIER ASSIGNMENT expression
    | IDENTIFIER LBRACKET expression RBRACKET ASSIGNMENT expression

expression -> expression LogicOp ExpressionM
    | ExpressionM

ExpressionM -> ExpressionS
    | ExpressionM Op ExpressionS

ExpressionS -> Element
    | ExpressionS PriOp Element

Element -> IDENTIFIER
    | REAL
    | INTEGER
    | BOOLEAN
    | STRING
    | CHAR
    | LPAREN expression RPAREN
    | InlineFuncCall
    | ArrayAccess
    | LENGTH LPAREN expression RPAREN

ArrayAccess -> IDENTIFIER LBRACKET expression RBRACKET

InlineFuncCall -> IDENTIFIER LPAREN param_expr_list RPAREN

LogicOp -> AND
    | OR

Op -> PLUS
    | MINUS
    | DIV
    | MOD
    | EQ
    | NEQ
    | LT
    | LTE
    | GT
    | GTE

PriOp -> TIMES
    | DIVISION

FuncCall -> IDENTIFIER LPAREN param_expr_list RPAREN

param_expr_list -> param_expr_list COMMA ParamExpr
    | ParamExpr

ParamExpr -> expression

IfStmt : IF expression THEN stmt ELSE stmt
    | IF expression THEN stmt

WhileStmt -> WHILE expression DO stmt

RepeatStmt -> REPEAT stmt UNTIL expression

ForStmt -> FOR Assignment TO expression DO stmt
    | FOR Assignment DOWNTO expression DO stmt

Writeln -> WRITELN LPAREN ElementList RPAREN

ElementList -> Element COMMA ElementList
    | Element

Readln -> READLN LPAREN ReadTargetList RPAREN

ReadTargetList -> ReadTarget COMMA ReadTargetList
    | ReadTarget

ReadTarget -> IDENTIFIER LBRACKET expression RBRACKET
    | IDENTIFIER

```
### Testes
Os testes feitos ao compilador construído fixam-se nos exemplos dados no pdf do projeto, que ao serem dados como input ao programa, mostram sucesso quando aplicados na máquina virtual

### Conclusão

O desenvolvimento do presente trabalho permitiu aplicar e consolidar diversos conceitos fundamentais da unidade curricular de Processamento de Linguagens, nomeadamente a utilização de Expressões Regulares, de reconhecedores Bottom-Up e o tratamento dos conflitos existentes na construção de um compilador.

Para além dos aspetos técnicos, este projeto evidenciou a importância de uma boa estruturação da gramática, bem como de uma adequada organização e cooperação em equipa. Por fim, mas não menos relevante, permitiu compreender melhor o engenho e a complexidade inerentes ao funcionamento dos compiladores existentes na atualidade.
