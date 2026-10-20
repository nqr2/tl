from dataclasses import dataclass

from tok import *
from lexer import lexer
from parse import *

text = """
import this.
"""

l = lexer(text)
a = parse(l)

print(a)
