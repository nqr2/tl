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


# ematch-case = unary
#             | {keyword argument}
def p_emcase(lexer):
    parts = []
    arguments = []
    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        parts = [name]
    else:
        while lexer.check(TokenTag.Keyword):
            p = lexer.expect(TokenTag.Keyword).payload[:-1]
            a = None

            if lexer.eat(TokenTag.LParen):
                arg = p_arg(lexer)
                lexer.expect(TokenTag.RParen)
            elif lexer.check(TokenTag.Identifier):
                arg_name = lexer.expect(TokenTag.Identifier).payload
                arg = syntax.Argument(name=arg_name)

            parts.append(p)
            arguments.append(a)

    lexer.expect(TokenTag.Equal)

    value = p_expr(lexer)

    return syntax.Matchcase_e(parts, arguments, value)


def p_ematch(lexer):
    discr = p_expr(lexer)
    lexer.expect(TokenTag.KWith)

    cases = []
    cases.append(p_emcase(lexer))

    while lexer.eat(TokenTag.Comma):
        cases.append(p_emcase(lexer))

    return syntax.Expr_Match(discr, cases)


def p_eprim(lexer):
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


def p_usend(lexer, recv=None, andq=False):
    recv = recv or p_eprim(lexer)

    if lexer.check(TokenTag.Identifier):
        op = lexer.expect(TokenTag.Identifier).payload
        return syntax.SendU(recv, op, andq)

    return recv


def p_binsend(lexer, recv=None, andq=False):
    recv = recv or p_usend(lexer, recv, andq)

    if lexer.check(TokenTag.Operator):
        op = lexer.expect(TokenTag.Operator).payload
        rhs = p_usend(lexer)

        return syntax.SendBin(recv, op, rhs, andq)

    return recv


def p_kwsend(lexer, recv=None, andq=False):
    recv = recv or p_binsend(lexer, recv, andq)

    parts = []
    args = []

    while lexer.check(TokenTag.Keyword):
        p = lexer.expect(TokenTag.Keyword).payload[:-1]
        a = p_binsend(lexer)

        parts.append(p)
        args.append(a)

    if len(parts) > 0:
        return syntax.Expr_SendKw(recv, parts, args, andq)
    else:
        return recv


# expr = 'int'
#      | 'pass'
#      | '(' expr { '.' expr } ')'
#      | 'identifier'
#      | 'match' {cases...}
def p_expr(lexer):
    p = p_kwsend(lexer)
    if p is not None:
        if lexer.eat(TokenTag.KThen):
            p2 = p_kwsend(lexer, recv=p)
            return p2

        if lexer.eat(TokenTag.KAnd):
            p2 = p_kwsend(lexer, recv=p, andq=True)
            return p2
        return p

    if lexer.eat(TokenTag.KMatch):
        return p_ematch(lexer)


# vardef = 'var' 'identifier' '=' expression.
def p_vardef(lexer):
    name = lexer.expect(TokenTag.Identifier).payload
    lexer.expect(TokenTag.Equal)
    value = p_expr(lexer)

    return syntax.VariableDefinition(name, value)


# ty(usage-side) = identifier.
def p_ty(lexer):
    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        return syntax.Type_Named(name)

    return None


# tycase = 'identifier'
#        | {keyword ty}
def p_tycase(lexer):
    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        return syntax.Matchcase_ty(parts=[name], arguments=[])

    parts = []
    arguments = []

    while lexer.check(TokenTag.Keyword):
        part = lexer.expect(TokenTag.Keyword).payload[:-1]
        arg = p_ty(lexer)

        parts.append(part)
        arguments.append(arg)

    return syntax.Matchcase_ty(parts, arguments)


# ty(definition-side) = ty(usage-side)
#                     | 'match' { case ,}
#                     | '{' {mem...} '}'
def p_tyd(lexer):
    defl = p_ty(lexer)
    if defl is not None:
        return defl

    if lexer.eat(TokenTag.KMatch):
        cases = []

        cases.append(p_tycase(lexer))

        while lexer.eat(TokenTag.Comma):
            cases.append(p_tycase(lexer))

        return syntax.Type_Match(cases)

    if lexer.eat(TokenTag.LCurl):
        rows = []

        if not lexer.check(TokenTag.RCurl):
            k = lexer.expect(TokenTag.Identifier).payload
            v = p_ty(lexer)
            rows.append(syntax.RowMember(k, v))

            while lexer.eat(TokenTag.Comma):
                k = lexer.expect(TokenTag.Identifier).payload
                v = p_ty(lexer)
                rows.append(syntax.RowMember(k, v))

        lexer.expect(TokenTag.RCurl)
        return syntax.Type_Row(rows)

    return None


# tydef = 'type' identifier '=' ty(definition-side)
def p_tydef(lexer):
    name = lexer.expect(TokenTag.Identifier).payload
    lexer.expect(TokenTag.Equal)
    value = p_tyd(lexer)

    return syntax.TypeDefinition(name, value)


# arg = identifier [type]
def p_arg(lexer):
    name = lexer.expect(TokenTag.Identifier).payload
    ty = p_ty(lexer)
    return syntax.Argument(name, ty=None)


def p_recv(lexer):
    lexer.expect(TokenTag.LParen)
    recv = p_arg(lexer)
    lexer.expect(TokenTag.RParen)
    return recv


# fndef = 'fn' [recv] identifier' ['(' {argument} ')'] [-> ty]  '=' expression.
#       | 'fn' [recv] { 'keyword' 'identifier' } [-> ty] '=' expression
def p_fndef(lexer):
    recv = None
    ret = None

    if lexer.check(TokenTag.LParen):
        recv = p_recv(lexer)

    if lexer.check(TokenTag.Keyword):
        name = []
        args = []

        while lexer.check(TokenTag.Keyword):
            name.append(lexer.expect(TokenTag.Keyword).payload[:-1])

            arg = None

            if lexer.eat(TokenTag.LParen):
                arg = p_arg(lexer)
                lexer.expect(TokenTag.RParen)
            elif lexer.check(TokenTag.Identifier):
                arg_name = lexer.expect(TokenTag.Identifier).payload
                arg = syntax.Argument(name=arg_name)

            args.append(arg)

        if lexer.eat(TokenTag.RArrow):
            ret = p_ty(lexer)

        lexer.expect(TokenTag.Equal)
        value = p_expr(lexer)

        return syntax.MessageDefinition(
            receiver=recv,
            message=syntax.MessageName_N(parts=name),
            arguments=args,
            returns=ret,
            value=value,
        )

    name = lexer.expect(TokenTag.Identifier).payload
    arguments = None

    if lexer.eat(TokenTag.LParen):
        arguments = []

        if not lexer.check(TokenTag.RParen):
            arguments.append(p_arg(lexer))

            while not lexer.check(TokenTag.RParen):
                lexer.expect(TokenTag.Comma)

                arguments.append(p_arg(lexer))

        lexer.expect(TokenTag.RParen)

    if lexer.eat(TokenTag.RArrow):
        ret = p_ty(lexer)

    lexer.expect(TokenTag.Equal)
    value = p_expr(lexer)

    return syntax.MessageDefinition(
        receiver=recv,
        message=syntax.MessageName_1(name),
        arguments=arguments,
        returns=ret,
        value=value,
    )


# toplevel = import | fndef | vardef.| tydef
def p_toplevel(lexer):
    if lexer.eat(TokenTag.KImport):
        return p_import(lexer)

    if lexer.eat(TokenTag.KVar):
        return p_vardef(lexer)

    if lexer.eat(TokenTag.KFn):
        return p_fndef(lexer)

    if lexer.eat(TokenTag.KType):
        return p_tydef(lexer)

    lexer.expect(TokenTag.Eof)


def parse(lexer):
    ac = []

    while not lexer.check(TokenTag.Eof):
        ac.append(p_toplevel(lexer))
        lexer.expect(TokenTag.Dot)

    return ac
