from tok import *
import syntax

# TODO: ast defs


# import = 'import' {'identifier'}
def p_import(lexer):
    p = []

    while lexer.check(TokenTag.Identifier):
        p.append(lexer.peek().payload)
        next(lexer)

    return syntax.Import(path=p)


# expr = 'int'
#      | 'pass'
#      | '(' expr { '.' expr } ')'
#      | 'identifier'
#      .
def p_expr(lexer):
    if lexer.check(TokenTag.Int):
        n = int(lexer.expect(TokenTag.Int).payload)
        return syntax.Expr_Int(n)

    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        return syntax.Expr_Variable(name)

    if lexer.eat(TokenTag.KPass):
        return syntax.Expr_Pass()

    if lexer.eat(TokenTag.LParen):
        units = []
        tail = p_expr(lexer)

        while lexer.eat(TokenTag.Dot):
            units.append(tail)
            tail = p_expr(lexer)

        lexer.expect(TokenTag.RParen)
        return syntax.Expr_Paren(units, tail)


# definition = msgdef | vardef.
# vardef = 'var' 'identifier' '=' expression.
# msgdef = 'identifier' '=' expression.
#        | { 'keyword' 'identifier' } '=' expression
def p_definition(lexer):
    if lexer.eat(TokenTag.KVar):
        name = lexer.expect(TokenTag.Identifier).payload
        lexer.expect(TokenTag.Equal)
        value = p_expr(lexer)

        return syntax.VariableDefinition(name, value)

    if lexer.check(TokenTag.Keyword):
        name = []
        args = []

        while lexer.check(TokenTag.Keyword):
            name.append(lexer.expect(TokenTag.Keyword).payload[:-1])

            arg_name = lexer.expect(TokenTag.Identifier).payload
            args.append(syntax.Argument(name=arg_name))

        lexer.expect(TokenTag.Equal)
        value = p_expr(lexer)

        return syntax.MessageDefinition(
            message=syntax.MessageName_N(parts=name), arguments=args, value=value
        )

    name = lexer.expect(TokenTag.Identifier).payload
    lexer.expect(TokenTag.Equal)
    value = p_expr(lexer)

    return syntax.MessageDefinition(
        message=syntax.MessageName_1(name), arguments=[], value=value
    )


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
