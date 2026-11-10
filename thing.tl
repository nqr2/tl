module(type T).

fn (x i32) factorial -> i32 = (
    var result = 1.
    (1 to: x) each: fn(i) (set result = result * i).
    result
).
