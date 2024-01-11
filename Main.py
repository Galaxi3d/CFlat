import Lexer

FILE_PATH = ''
file = open('FILE_PATH', 'r')
text = file.read().splitlines()
Lexer.Lexer(text)
