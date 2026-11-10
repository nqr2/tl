import pprint as pp

from lexer import lexer
from parse import parse

text = open("thing.tl").read()

l = lexer(text)
a = parse(l)

pp.pp(a)
