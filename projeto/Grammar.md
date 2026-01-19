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


