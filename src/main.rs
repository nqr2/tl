mod lexer;
mod token;

use std::fs::read_to_string;

fn main() -> std::io::Result<()> {
    let file = read_to_string("thing.tl")?;

    for t in lexer::Lexer::new(&file) {
        println!("{:?}", t);
    }

    Ok(())
}
