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
class Extends:
    path: [str]


@dataclass
class Argument:
    name: str
    ty: Type = None  # TODO


@dataclass
class MessageDefinition:
    receiver: (str, Type)
    generics: [str]
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
class Expr_Set:
    lv: Expr
    rv: Expr


@dataclass
class Expr_Lambda:
    args: [Argument]
    units: [Expr]
    tail: Expr


@dataclass
class Expr_Paren:
    units: [Expr]
    tail: Expr


@dataclass
class Matchcase_e:
    parts: [str]
    arguments: [(str, Type)]
    value: Expr


@dataclass
class Expr_Match:
    discriminated: Expr
    cases: [Matchcase_e]


@dataclass
class Expr_SendKw:
    recv: Expr
    parts: [str]
    args: [Expr]
    andq: bool = False


class MExpr:
    pass


@dataclass
class MArg_Ty:
    name: str


@dataclass
class MArg_Mod:
    name: str


@dataclass
class MExpr_Struct:
    mems: [any]


@dataclass
class ModuleDefinition:
    name: str
    args: [any]
    value: MExpr


@dataclass
class Expr_SendU:
    recv: Expr
    op: str
    andq: bool = False


@dataclass
class Expr_SendBin:
    recv: Expr
    op: str
    rhs: Expr
    andq: bool = False
