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

var PI = 3.14592.
var sixteen = 16r10.
var fifteen = 2r1111.
var million = 1.0e6.

fn (self char) newline? -> bool =
    self == `\n`.

fn (self char) nul? -> bool =
    self == `\x00`.
