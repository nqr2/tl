#[extern] decl (l i32) + (r i32) -> i32.

fn add(l, r) -> i32 =
    l + r.

fn five -> i32 = add(2, 3).
