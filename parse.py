from tok import *
import syntax


# extends = 'extends' path
def p_extends(lexer):
    p = []

    while lexer.check(TokenTag.Identifier):
        p.append(lexer.peek().payload)
        next(lexer)

    return syntax.Extends(path=p)


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
                arg = syntax.Argument(labelq=False, name=arg_name)

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


def p_eprim_nc(lexer):
    if lexer.eat(TokenTag.KDo):
        inner = p_eprim_nc(lexer)
        return syntax.Expr_Do(inner)

    if lexer.check(TokenTag.String):
        n = lexer.expect(TokenTag.String).payload
        return syntax.Expr_Str(n)

    if lexer.check(TokenTag.Char):
        n = lexer.expect(TokenTag.Char).payload
        return syntax.Expr_Char(n)

    if lexer.check(TokenTag.Int):
        n = int(lexer.expect(TokenTag.Int).payload)
        return syntax.Expr_Int(n)

    if lexer.check(TokenTag.Float):
        n = lexer.expect(TokenTag.Float).payload
        return syntax.Expr_Flt(n)

    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        return syntax.Expr_Variable(name)

    if lexer.eat(TokenTag.Hash):
        recv = None
        parts = []

        if lexer.eat(TokenTag.LParen):
            recv = p_ty(lexer)
            lexer.expect(TokenTag.RParen)

        if lexer.check({TokenTag.Identifier, TokenTag.Operator}):
            parts = [lexer.expect({TokenTag.Identifier, TokenTag.Operator}).payload]
        else:
            while lexer.check(TokenTag.Keyword):
                parts.append(lexer.expect(TokenTag.Keyword).payload)

        return syntax.Expr_MsgRef(recv, parts)

    if lexer.eat(TokenTag.LCurl):

        def l_rrow(l):
            k = l.expect(TokenTag.Identifier).payload
            l.expect(TokenTag.Equal)
            v = p_expr(l)
            return (k, v)

        rows = []

        if not lexer.check(TokenTag.RCurl):
            rows.append(l_rrow(lexer))

            while lexer.eat(TokenTag.Comma):
                rows.append(l_rrow(lexer))

        lexer.expect(TokenTag.RCurl)
        return syntax.Expr_Row(rows)

    if lexer.eat(TokenTag.KPass):
        return syntax.Expr_Pass()

    if lexer.eat(TokenTag.KFn):
        args = []

        if lexer.eat(TokenTag.LParen):
            args.append(p_arg(lexer))

            while lexer.eat(TokenTag.Comma):
                args.append(p_arg(lexer))

            lexer.expect(TokenTag.RParen)

        tail = p_eprim(lexer)
        return syntax.Expr_Lambda(args, [], tail)

    if lexer.eat(TokenTag.LParen):
        units = []
        tail = p_expr(lexer)

        while lexer.eat(TokenTag.Dot):
            units.append(tail)
            tail = p_expr(lexer)

        lexer.expect(TokenTag.RParen)
        return syntax.Expr_Paren(units, tail)


def p_eprim(lexer):
    p = p_eprim_nc(lexer)

    while lexer.eat(TokenTag.LParen):
        args = []

        if not lexer.check(TokenTag.RParen):
            args.append(p_expr(lexer))

            while lexer.eat(TokenTag.Comma):
                args.append(p_expr(lexer))

        lexer.expect(TokenTag.RParen)
        p = syntax.Expr_Call(p, args)

    while lexer.eat(TokenTag.KAs):
        t = p_ty(lexer)
        p = syntax.Expr_As(p, t)

    return p


def p_usend(lexer, recv=None, andq=False):
    recv = recv or p_eprim(lexer)

    while lexer.check(TokenTag.Identifier):
        op = lexer.expect(TokenTag.Identifier).payload
        recv = syntax.Expr_SendU(recv, op, andq)

    return recv


def p_binsend(lexer, recv=None, andq=False):
    recv = p_usend(lexer, recv, andq)

    while lexer.check(TokenTag.Operator):
        op = lexer.expect(TokenTag.Operator).payload
        rhs = p_usend(lexer)

        recv = syntax.Expr_SendBin(recv, op, rhs, andq)

    return recv


def p_kwsend(lexer, recv=None, andq=False):
    recv = p_binsend(lexer, recv, andq)

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
        while True:
            print(lexer.peek())

            if lexer.eat(TokenTag.KThen):
                p = p_kwsend(lexer, recv=p)
                continue

            if lexer.eat(TokenTag.KAnd):
                p = p_kwsend(lexer, recv=p, andq=True)
                continue

            return p

    if lexer.eat(TokenTag.KVar):
        return p_vardef(lexer)

    if lexer.eat(TokenTag.KConst):
        return p_vardef(lexer, False)

    if lexer.eat(TokenTag.KMatch):
        return p_ematch(lexer)

    if lexer.eat(TokenTag.At):
        inner = p_expr(lexer)
        return syntax.Expr_Load(inner)

    if lexer.eat(TokenTag.KSet):
        lv = p_expr(lexer)
        lexer.expect(TokenTag.Equal)
        rv = p_expr(lexer)
        return syntax.Expr_Set(lv, rv)

    if lexer.eat(TokenTag.KLabel):
        name = lexer.expect(TokenTag.Identifier).payload
        ty = p_ty(lexer)

        if ty is not None:
            lexer.expect(TokenTag.KWith)

        v = p_expr(lexer)
        return syntax.Expr_Label(name, ty, v)

    if lexer.eat(TokenTag.KBreak):
        name = lexer.expect(TokenTag.Identifier).payload
        v = None

        if lexer.eat(TokenTag.KWith):
            v = p_expr(lexer)

        return syntax.Expr_Break(name, v)


# vardef = 'var' 'identifier' '=' expression.
def p_vardef(lexer, mutq=True):
    name = lexer.expect(TokenTag.Identifier).payload
    lexer.expect(TokenTag.Equal)
    value = p_expr(lexer)

    return syntax.VariableDefinition(mutq, name, value)


# ty(usage-side) = identifier | fn(args...) [-> ty]
def p_ty(lexer):
    if lexer.eat(TokenTag.At):
        constq = lexer.eat(TokenTag.KConst)
        inner = p_ty(lexer)
        return syntax.Type_Ptr(constq, inner)

    if lexer.check(TokenTag.Identifier):
        name = lexer.expect(TokenTag.Identifier).payload
        return syntax.Type_Named(name)

    if lexer.eat(TokenTag.LBrac):
        n = lexer.expect(TokenTag.Int).payload
        lexer.expect(TokenTag.RBrac)
        inner = p_ty(lexer)
        return syntax.Type_Arr(n, inner)

    if lexer.eat(TokenTag.KFn):
        args = []
        ret = None

        if lexer.eat(TokenTag.LParen):
            if not lexer.eat(TokenTag.RParen):
                args.append(p_ty(lexer))
                while lexer.eat(TokenTag.Comma):
                    args.append(p_ty(lexer))
            lexer.expect(TokenTag.RParen)

        if lexer.eat(TokenTag.RArrow):
            ret = p_ty(lexer)
        return syntax.Type_Fn(args, ret)

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
def p_tydef(lexer, indecl=False):
    name = lexer.expect(TokenTag.Identifier).payload

    if indecl and not lexer.check(TokenTag.Equal):
        return syntax.TypeAbstract(name)

    lexer.expect(TokenTag.Equal)
    value = p_tyd(lexer)

    return syntax.TypeDefinition(name, value)


# arg = identifier [type]
def p_arg(lexer):
    labelq = lexer.eat(TokenTag.KLabel)
    name = lexer.expect(TokenTag.Identifier).payload
    ty = p_ty(lexer)
    return syntax.Argument(labelq=labelq, name=name, ty=ty)


def p_recv(lexer):
    lexer.expect(TokenTag.LParen)
    recv = p_arg(lexer)
    lexer.expect(TokenTag.RParen)
    return recv


# fndef = 'decl' [recv] identifier' ['(' {argument} ')'] [-> ty]
#       | 'decl' [recv] { 'keyword' 'identifier' } [-> ty]
def p_fndecl(lexer):
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
                arg = syntax.Argument(labelq=False, name=arg_name)

            args.append(arg)

        if lexer.eat(TokenTag.RArrow):
            ret = p_ty(lexer)

        return syntax.MessageDeclaration(
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

    return syntax.MessageDeclaration(
        receiver=recv,
        message=syntax.MessageName_1(name),
        arguments=arguments,
        returns=ret,
    )


# fndef = 'fn' [gen] [recv] identifier' ['(' {argument} ')'] [-> ty]  '=' expression.
#       | 'fn' [gen] [recv] { 'keyword' 'identifier' } [-> ty] '=' expression
def p_fndef(lexer):
    recv = None
    ret = None
    gens = []

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
                arg = syntax.Argument(labelq=False, name=arg_name)

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


def p_mpexpr(lexer, insig=False):
    if lexer.eat(TokenTag.LCurl):
        mems = []

        if not lexer.check(TokenTag.RCurl):
            mems.append(p_toplevel(lexer, insig))

            while lexer.eat(TokenTag.Dot):
                mems.append(p_toplevel(lexer, insig))

        lexer.expect(TokenTag.RCurl)
        return syntax.MExpr_Struct(mems)

    if lexer.check(TokenTag.Identifier):
        return syntax.MExpr_Named(lexer.expect(TokenTag.Identifier).payload)


def p_mexpr(lexer, insig=False):
    p = p_mpexpr(lexer, insig)

    while lexer.eat(TokenTag.LParen):
        args = []

        if not lexer.check(TokenTag.RParen):
            args.append(p_marg(lexer))

            while lexer.eat(TokenTag.Comma):
                args.append(p_marg(lexer))

        lexer.expect(TokenTag.RParen)

        p = syntax.MExpr_Call(p, args)

    return p


def p_marg(lexer):
    if lexer.eat(TokenTag.KType):
        name = p_ty(lexer)
        return syntax.MArg_Ty(name)

    name = p_mexpr(lexer)
    return syntax.MArg_Mod(name)


def p_mdef(lexer):
    if lexer.eat(TokenTag.LParen):
        args = []

        if not lexer.check(TokenTag.RParen):
            args.append(p_marg(lexer))

            while lexer.eat(TokenTag.Comma):
                args.append(p_marg(lexer))

        lexer.expect(TokenTag.RParen)

        return syntax.ModuleParams(args)

    args = []
    in_sig = False

    if lexer.eat(TokenTag.KType):
        in_sig = True

    name = lexer.expect(TokenTag.Identifier).payload

    if lexer.eat(TokenTag.LParen):
        if not lexer.check(TokenTag.RParen):
            args.append(p_marg(lexer))

            while lexer.eat(TokenTag.Comma):
                args.append(p_marg(lexer))

        lexer.expect(TokenTag.RParen)

    lexer.expect(TokenTag.Equal)
    value = p_mexpr(lexer, in_sig)

    if in_sig:
        return syntax.SigDefinition(name, args, value)

    return syntax.ModuleDefinition(name, args, value)


def p_attrs(lexer):
    # attr = identifier
    def attr(l):
        return l.expect(TokenTag.Identifier).payload

    a = []
    lexer.expect(TokenTag.LBrac)

    if not lexer.check(TokenTag.RBrac):
        a.append(attr(lexer))
        while lexer.eat(TokenTag.Comma):
            a.append(attr(lexer))

    lexer.expect(TokenTag.RBrac)
    return a


# toplevel = import | fndecl | fndef | vardef.| tydef | mdef | attrs toplevel
def p_toplevel(lexer, insig=False):
    if lexer.eat(TokenTag.Hash):
        attr = p_attrs(lexer)
        inner = p_toplevel(lexer)
        return syntax.Attrlist(attr, inner)

    if lexer.eat(TokenTag.KExtends):
        return p_extends(lexer)

    if lexer.eat(TokenTag.KImport):
        return p_import(lexer)

    if lexer.eat(TokenTag.KDecl):
        return p_fndecl(lexer)

    if lexer.eat(TokenTag.KVar):
        return p_vardef(lexer)

    if lexer.eat(TokenTag.KConst):
        return p_vardef(lexer, False)

    if lexer.eat(TokenTag.KFn):
        return p_fndef(lexer)

    if lexer.eat(TokenTag.KType):
        return p_tydef(lexer, insig)

    if lexer.eat(TokenTag.KModule):
        return p_mdef(lexer)

    lexer.expect(TokenTag.Eof)


def parse(lexer):
    ac = []

    while not lexer.check(TokenTag.Eof):
        ac.append(p_toplevel(lexer))
        lexer.expect(TokenTag.Dot)

    return ac
