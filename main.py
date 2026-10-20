from dataclasses import dataclass

from tok import *
from lexer import lexer
from parse import *

text = """
import this.

two = 2.
unit = pass.
two2 = (2).
pass-two = (pass. pass. 2).
"""

l = lexer(text)
a = parse(l)

print(a)
