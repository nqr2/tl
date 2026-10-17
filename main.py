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
        ("LArrow", "<-"),
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
        ("KIf", "if"),
        ("KElse", "else"),
        ("KWhile", "while"),
        ("KLoop", "loop"),
        ("KVar", "var"),
        ("KConst", "const"),
        ("KExport", "export"),
        ("KMatch", "match"),
        ("KEnum", "enum"),
        ("KRecord", "record"),
        ("KReturn", "return"),
        ("KAnd", "and"),
        ("KThen", "then"),
        ("Unknown", "<unknown>"),
    ],
)


@dataclass
class Token:
    tag: TokenTag
    start: int
    end: int
    payload: any = None


class Peek:
    def __init__(self, inner):
        self._inner = inner
        self._peek = None
        self.pos = 0

    def peek(self):
        if self._peek is None:
            self._peek = next(self._inner)

        return self._peek

    def __next__(self):
        self.pos += 1
        if self._peek is not None:
            tmp, self._peek = self._peek, None
            return tmp

        return next(self._inner)


SINGLE_PUNCTUATION = "()[]{},.;:#"
PUNCTUATION = "?!+-&/%$@^<>*"


def lexer(text):
    head = Peek(iter(text))

    try:
        while True:
            here = head.pos

            if head.peek().isspace():
                while head.peek().isspace():
                    next(head)
                continue

            if head.peek() in SINGLE_PUNCTUATION:
                s = next(head)
                yield Token(tag=TokenTag(s), start=here, end=head.pos)
                continue

            if head.peek() == '"':
                next(head)

                while head.peek() != '"':
                    next(head)

                next(head)

                word = text[here : head.pos]

                yield Token(
                    tag=TokenTag.Comment, start=here, end=head.pos, payload=word
                )
                continue

            if head.peek() == "'":
                next(head)

                while head.peek() != "'":
                    next(head)

                next(head)

                word = text[here : head.pos]

                yield Token(tag=TokenTag.String, start=here, end=head.pos, payload=word)
                continue

            if head.peek() in PUNCTUATION:
                while head.peek() in PUNCTUATION:
                    next(head)

                word = text[here : head.pos]
                tag = TokenTag.Operator if word not in TokenTag else TokenTag(word)

                yield Token(tag=tag, start=here, end=head.pos, payload=word)
                continue

            if head.peek().isalpha() or head.peek() in "_":
                while head.peek().isalnum() or head.peek() in "_-":
                    next(head)

                if head.peek() == ":":
                    next(head)

                    yield Token(tag=TokenTag.Keyword, start=here, end=head.pos)

                    continue

                if head.peek() in "!?'":
                    next(head)

                word = text[here : head.pos]
                tag = TokenTag.Identifier if word not in TokenTag else TokenTag(word)

                yield Token(tag=tag, start=here, end=head.pos, payload=word)

                continue

            if head.peek() in "0123456789":
                while head.peek() in "0123456789":
                    next(head)

                word = text[here : head.pos]
                yield Token(
                    tag=TokenTag.Int, start=here, end=head.pos, payload=int(word)
                )
                continue

            s = next(head)
            yield Token(tag=TokenTag.Unknown, start=here, end=head.pos, payload=s)
    except StopIteration:
        pass


text = """
import (2) of: "some" other-stuff.
left <- one <*> two or? five.
"""

for token in lexer(text):
    print(token)
