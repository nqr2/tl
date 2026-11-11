import pprint as pp

from lexer import lexer
from parse import parse

import hir

h = hir.Block()
print(h.add_u32(0, 0))
print(h[hir.Ref(0)])

exit(0)

text = open("thing.tl").read()

l = lexer(text)
a = parse(l)

pp.pp(a)
