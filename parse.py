from tok import *


# import = 'import' path '.'
# path = {unary} .
def p_import(lexer):
    p = []
    while lexer.check(TokenTag.Identifier):
        p.append(lexer.peek().payload)
        next(lexer)
    lexer.expect(TokenTag.Dot)
    return {"type": "import", "path": p}

# toplevel = import.
def p_toplevel(lexer):
    if lexer.eat(TokenTag.KImport):
        return p_import(lexer)

    lexer.expect(TokenTag.Eof)

def parse(lexer):
    ac = []
    while not lexer.check(TokenTag.Eof):
        ac.append(p_toplevel(lexer))
    return ac
