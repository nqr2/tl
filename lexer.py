from tok import *


class Peek:
    def __init__(self, inner):
        self._inner = inner
        self._peek = None
        self.pos = 0

    def peek(self):
        if self._peek is None:
            self._peek = next(self._inner)

        return self._peek

    def __iter__(self):
        return self

    def __next__(self):
        self.pos += 1
        if self._peek is not None:
            tmp, self._peek = self._peek, None
            return tmp

        return next(self._inner)


@dataclass
class ExpectFailure(Exception):
    expected: TokenTag
    got: TokenTag
    span: (int, int)

    def __str__(self):
        return f"at {self.span} expected {self.expected}, got {self.got}"


class Lexer(Peek):
    def __init__(self, x):
        super(Lexer, self).__init__(x)

    def check(self, tag):
        got = self.peek().tag
        return got == tag

    def eat(self, tag):
        p = self.check(tag)
        if p:
            next(self)
        return p

    def expect(self, tag):
        got = self.peek()
        if not self.eat(tag):
            raise ExpectFailure(span=(got.start, got.end), expected=tag, got=got.tag)
        return got


SINGLE_PUNCTUATION = "()[]{},.;:#"
PUNCTUATION = "?!+-&/%$@^<>*="


def lexer_(text):
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

                if head.peek() in "!?#":
                    next(head)

                if head.peek() == ":":
                    next(head)

                    yield Token(tag=TokenTag.Keyword, start=here, end=head.pos)

                    continue

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
        yield Token(tag=TokenTag.Eof, start=0, end=0, payload="")


def lexer(text):
    return Lexer(lexer_(text))
