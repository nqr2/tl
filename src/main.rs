mod combinator;
mod lexer;
mod lexer_wrapper;
mod token;

use std::fs::read_to_string;

fn main() -> std::io::Result<()> {
    let file = read_to_string("thing.tl")?;

    for t in lexer::Lexer::new(&file) {
        println!("{:?}", t);
    }

    Ok(())
}
