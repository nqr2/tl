import this.

fn two = 2.
fn unit = pass.
fn two2 = (2).
fn pass-two = (pass. 2).

fn (x i32) asZero -> i32 = 0.

var global = 16.
fn reads = global.

fn either: x or: y = x.

fn funcy(x) = x.

"nvm i forgot these were comments (woops)"

type MaybeInt = match
    Nothing,
    Some: i32.

type IntPair = {l i32, r i32}.

fn (x MaybeInt) unwrapOr: (default i32) -> i32 =
    match x with
        Nothing = default,
        Some: x = x.

var five = MaybeInt Some: 3 then unwrapOr: 0.
