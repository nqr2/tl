# desugared or smth

from dataclasses import dataclass
from enum import Enum

BasicType = Enum(
    "BasicType",
    [
        ("unit", "unit"),
        ("u8", "u8"),
        ("u16", "u16"),
        ("u32", "u32"),
        ("u64", "u64"),
        ("s8", "s8"),
        ("s16", "s16"),
        ("s32", "s32"),
        ("s64", "s64"),
        ("f32", "f32"),
        ("f64", "f64")
    ],
)

@dataclass
class Const:
    value: any

@dataclass
class Operation:
    operation: str
    arguments: [any]

@dataclass
class Ref:
    index: int

@dataclass
class BlockRef:
    index: int

class Block:
    def __init__(self):
        self._ops = []
        self._fwd = []

    def __getitem__(self, r: Ref):
        return self._ops[r.index]

    def find(self, n):
        if isinstance(n,Ref):
            n = n.index

        while self._fwd[n] != -1:
            n = self._fwd[n]

        return n

    def union(self, target: Ref, source: Ref):
        t = self.find(target)
        self._fwd[t] = source.index

    def _define_operation(name, n_args):
        def wrap(k):
            if isinstance(k,Operation):
                raise RuntimeError("argument should be a constant or a Ref to another operation")

            if type(k) not in {Const,Ref}:
                return Const(k)

            return k

        def inner(self, *args):
            op = Operation(name, [wrap(a) for a in args])
            assert len(op.arguments) == n_args

            self._ops.append(op)
            self._fwd.append(-1)

            return Ref(len(self._ops)-1)

        return inner

    nop = _define_operation('nop', 0)
    add_u32 = _define_operation('add.u32', 2)

class Function:
    def __init__(self, arguments, returns):
        self._blocks = []
        self._entry = None
        self.arguments = arguments
        self.returns = returns

    def make_entry(self, ref: BlockRef):
        self._entry = ref

    def new_block(self):
        b = Block()
        self._blocks.append(b)
        return BlockRef(len(self._blocks)-1)
