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

"module stuff"

module M = {
    var x = 5
}.

import M.

var mx = M x.

module N = {
    extends M.
    var y = 6
}.

module Option(type T) = {
    type t = match
        None,
        Some: T
}.

type Bool = match False, True.

"yippie?"
fn generic(T) (b Bool) if: (t T) else: (f T) -> T =
  match b with
    False = f,
    True = t.

fn fact(x i32) -> i32 = (
    var result = 1.

    (1 to: x) each: fn(i) {
        set result = result * i as i32
    }.

    result
).

fn fail(from Bool, label to i32) -> i32 =
    match from with
        False = break to with 0,
        True = break to with 1.

fn wontfail(by Bool) -> i32 =
    label to i32 with
    fail(by, to).
