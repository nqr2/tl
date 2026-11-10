module(type T).

fn (x i32) factorial -> i32 = (
    var result = 1.
    (1 to: x) each: fn(i) (set result = result * i).
    result
).

"it's all function pointers anyway, so no issues there"
type lazy = fn -> T.

fn (self lazy) force -> T = self().

fn remote-set!(target @i32, source i32) =
    set @target = source.

#[extern] decl puts(_ @const u8).

fn example = (
    puts('hello, example!' as-bytes)
).

fn (self char) is-newline -> bool =
    self == `N`.

fn maybe = "maybe this works well enough? who knows"
    Option(pass) Some: pass then unwrapOr: pass.

const PI = 3.14592.
const sixteen = 16r10.
const fifteen = 2r1111.
const million = 1.0e6.

fn (self char) newline? -> bool =
    self == `\n`.

fn (self char) nul? -> bool =
    self == `\x00`.

fn tauto(_ char)->bool = true.

fn predicate_off(the bool) -> fn(char)->bool =
    match the with
        True  = #(char)newline?,  " #(receiver type) message "
        False = #tauto.           " #message "
        "since we don't have overloading just the name works"

fn (x bool) id -> bool = x.

const t = True then id then id then id then id.
