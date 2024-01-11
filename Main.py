import Lexer

FILE_PATH = ''
file = open('FILE_PATH', 'r')
text = file.read().splitlines()
variables = {}
functions = {}
Lexer.Lexer(text)
