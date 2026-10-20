from dataclasses import dataclass
from enum import Enum, Flag


class MessageName:
    pass


@dataclass
class MessageName_1(MessageName):  # either binary or unary names
    name: str


@dataclass
class MessageName_N(MessageName):  # keywords
    parts: [str]


@dataclass
class Import:
    path: [str]


@dataclass
class Argument:
    name: str
    ty: any = None  # TODO


@dataclass
class MessageDefinition:
    message: MessageName
    arguments: [str]
    value: Expr


@dataclass
class VariableDefinition:
    name: str
    value: Expr


class Expr:
    pass


@dataclass
class Expr_Variable:  # or unary msg
    name: str


@dataclass
class Expr_Int:
    value: int


@dataclass
class Expr_Pass:
    pass


@dataclass
class Expr_Paren:
    units: [Expr]
    tail: Expr
