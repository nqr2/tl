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
    labelq: bool
    name: str
    ty: Type = None  # TODO


@dataclass
class Expr_Break:
    label: str
    val: Expr = None


@dataclass
class Expr_Call:
    recv: Expr
    args: [Expr]


@dataclass
class Expr_Do:
    inner: Expr


@dataclass
class Attrlist:
    attrs: [str]
    wrapping: any


@dataclass
class MessageDeclaration:
    receiver: (str, Type)
    message: MessageName
    arguments: [Argument]
    returns: Type


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
class VariableDeclaration:
    name: str


@dataclass
class TypeDefinition:
    name: str
    value: Type


@dataclass
class TypeAbstract:
    name: str


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


@dataclass
class Type_Fn:
    args: [Type]
    ret: Type


@dataclass
class Type_Ptr:
    inner: Type


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
class Expr_Load:
    inner: Expr


@dataclass
class Expr_Str:
    inner: str


@dataclass
class Expr_Char:
    inner: str


@dataclass
class Expr_Set:
    lv: Expr
    rv: Expr


@dataclass
class Expr_As:
    rv: Expr
    ty: Type


@dataclass
class Expr_Label:
    n: str
    t: Type
    v: Expr


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
class ModuleParams:
    params: [any]


@dataclass
class SigDefinition:
    name: str
    args: [any]
    value: MExpr


@dataclass
class Expr_Row:
    rows: [(str, Expr)]


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
