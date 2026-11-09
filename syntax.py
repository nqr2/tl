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
    ty: Type = None  # TODO


@dataclass
class MessageDefinition:
    receiver: (str, Type)
    message: MessageName
    arguments: [Argument]
    returns: Type
    value: Expr


class Type:
    pass


@dataclass
class Type_Named:
    name: str


@dataclass
class VariableDefinition:
    name: str
    value: Expr


@dataclass
class TypeDefinition:
    name: str
    value: Type


@dataclass
class Matchcase_ty:
    parts: [str]
    arguments: [Type]


@dataclass
class Type_Match:
    cases: [Matchcase_ty]


@dataclass
class RowMember:
    name: str
    ty: Type


@dataclass
class Type_Row:
    rows: [RowMember]


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
