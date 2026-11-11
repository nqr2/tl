module Array4(type T) = {
    type inner = [4]T
}.

module Array4_I32 = Array4(type i32).
