from dataclasses import dataclass
from enum import Enum

TokenTag = Enum(
    "TokenTag",
    [
        ("Eof", "<eof>"),
        ("Identifier", "<identifier>"),
        ("Keyword", "<keyword>"),
        ("Operator", "<operator>"),
        ("LParen", "("),
        ("RParen", ")"),
        ("LBrac", "["),
        ("RBrac", "]"),
        ("Comment", "<comment>"),
        ("Equal", "="),
        ("RArrow", "->"),
        ("LCurl", "{"),
        ("RCurl", "}"),
        ("Hash", "#"),
        ("Comma", ","),
        ("Semicolon", ";"),
        ("Colon", ":"),
        ("Dot", "."),
        ("String", "<string>"),
        ("Char", "<character>"),
        ("Int", "<integer>"),
        ("Float", "<float>"),
        ("KModule", "module"),
        ("KImport", "import"),
        ("KType", "type"),
        ("KVar", "var"),
        ("KConst", "const"),
        ("KExport", "export"),
        ("KMatch", "match"),
        ("KWith", "with"),
        ("KSet", "set"),
        ("KLabel", "label"),
        ("KBreak", "break"),
        ("KAnd", "and"),
        ("KThen", "then"),
        ("KAs", "as"),
        ("KPass", "pass"),
        ("KFn", "fn"),
        ("KDo", "do"),
        ("KGeneric", "generic"),
        ("KExtends", "extends"),
        ("Unknown", "<unknown>"),
    ],
)


@dataclass
class Token:
    tag: TokenTag
    start: int
    end: int
    payload: any = None
