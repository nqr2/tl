from dataclasses import dataclass

from tok import *
from lexer import lexer
from parse import *

text = """
import this.
two = 2.
unit = pass.
two2 = (2).
pass-two = (pass. 2).
var global = 16.
reads = global.
either: x or: y = x.
"""

l = lexer(text)
a = parse(l)

print(a)
