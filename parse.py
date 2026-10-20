from tok import *

# TODO: ast defs


# import = 'import' path
# path = {unary} .
def p_import(lexer):
    p = []
    while lexer.check(TokenTag.Identifier):
        p.append(lexer.peek().payload)
        next(lexer)
    return {"type": "import", "path": p}


# expr = 'int'
#      | 'pass'
#      | '(' expr { '.' expr } ')'
#      .
def p_expr(lexer):
    if lexer.check(TokenTag.Int):
        n = int(lexer.expect(TokenTag.Int).payload)
        return {"type": "int", "value": n}

    if lexer.eat(TokenTag.KPass):
        return {"type": "pass"}

    if lexer.eat(TokenTag.LParen):
        units = []
        tail = p_expr(lexer)

        while lexer.eat(TokenTag.Dot):
            units.append(tail)
            tail = p_expr(lexer)

        lexer.expect(TokenTag.RParen)
        return {"type": "paren", "units": units, "tail": tail}


# definition = msgdef.
# msgdef = identifier '=' expression.
def p_definition(lexer):
    name = lexer.expect(TokenTag.Identifier).payload
    lexer.expect(TokenTag.Equal)
    value = p_expr(lexer)
    return {"type": "msgdef", "msg": name, "value": value}


# toplevel = import | definition.
def p_toplevel(lexer):
    if lexer.eat(TokenTag.KImport):
        return p_import(lexer)

    if not lexer.check(TokenTag.Eof):
        return p_definition(lexer)

    lexer.expect(TokenTag.Eof)


def parse(lexer):
    ac = []
    while not lexer.check(TokenTag.Eof):
        ac.append(p_toplevel(lexer))
        lexer.expect(TokenTag.Dot)
    return ac
