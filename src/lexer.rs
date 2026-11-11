use crate::token::*;
use std::{iter::Peekable, str::Chars};

pub enum Error {}

struct Lexer<'a> {
    text: &'a str,
    head: Peekable<Chars<'a>>,
    position: usize,
}

impl<'a> Lexer<'a> {
    pub fn new(text: &'a str) -> Self {
        Self {
            text,
            head: text.chars().peekable(),
            position: 0,
        }
    }

    fn lex(&mut self) -> Result<Token<'a>, Error> {
        todo!()
    }
}

impl<'a> Iterator for Lexer<'a> {
    type Item = Result<Token<'a>, Error>;

    fn next(&mut self) -> Option<Self::Item> {
        match self.lex() {
            Ok(t) => {
                if t.tag == Tag::Eof {
                    None
                } else {
                    Some(Ok(t))
                }
            }
            e => Some(e),
        }
    }
}
