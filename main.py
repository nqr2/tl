from dataclasses import dataclass

from tok import *
from lexer import lexer
from parse import *

text = open("thing.tl").read()

l = lexer(text)
a = parse(l)

print(a)
