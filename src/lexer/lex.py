#List of token names
tokens = (

	#symbols
	'INT',
	'STRING',
	'ID',

	#ignored symbols the lexer or parser shouldn't mind
	#'NEW_LINE',
	#'TAB',
	#'SPACE',
	'COMMENT',

	#punctuation symbols
	'COMMA',
	'COLON',
	'SEMICOLON',
	'LPAREN',
	'RPAREN',
	'LBRACK',
	'RBRACK',
	'LBRACE',
	'RBRACE',
	'DOT',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'EQ',
	'NEQ',
	'LT',
	'LE',
	'GT',
	'GE',
	'AND',
	'OR',
	'ASSIGN',

	#keywords
	'ARRAY',
	'IF',
	'THEN',
	'ELSE',
	'WHILE',
	'FOR',
	'TO',
	'DO',
	'LET',
	'IN',
	'END',
	'OF',
	'BREAK',
	'NIL',
	'FUNCTION',
	'VAR',
	'TYPE',
)

reservedKeywords = (
	'array',
	'if',
	'then',
	'else',
	'while',
	'for',
	'to',
	'do',
	'let',
	'in',
	'end',
	'of',
	'break',
	'nil',
	'function',
	'var',
	'type',
)

# Regular expression rules with some actions required
# Reads an integer value
def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

# reads
t_STRING = r'\"([^\\\"]|(\\n)|(\\t)|(\\\^c)|(\\[0-9][0-9][0-9])|(\\\")|(\\\\)|(\\[\s\t\n\f]+\\))*\"'

def t_ID(t):
	r'[a-zA-Z][a-zA-Z_0-9]*'
	if t.value in reservedKeywords:
		t.type = t.value.upper()
	return t

# Regular expression rules for simple tokens
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LPARE = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'\='
t_NEQ = r'\<\>'
t_LT = r'\<'
t_LE = r'\<\='
t_GT = r'\>'
t_GE = r'\>\='
t_AND = r'\%'
t_OR = r'\|'
t_ASSIGN = r'\:\='

# Define a rule so we can track line numbers
def T_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Esto funciona correctamente?
t_ignore_COMMENT = r'\/\*.*\*\/'

# Error handling rule
def t_error(t):
	print("Illegal character '%s' " %t.value[0])
	t.lexer.skip(1)


if __name__ == '__main__':
	# Build the lexer
	from .ply import lex as lex
	import sys

	lexer = lex.lex()

	if len(sys.argv) > 1:
		f = open(sys.argv[1],"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break

	lex.input(data)

	# Tokenize
	while True:
		tok = lex.token()
		if not tok:
			break      # No more input
		print(tok)
