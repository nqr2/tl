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

#[extern] decl puts(_ @u8).

fn example = (
    puts('hello, example!' as-bytes)
).

fn (self char) is-newline -> bool =
    self == `N`.
