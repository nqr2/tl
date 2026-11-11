// i'm not porting everything as-is, time for combinators or smth

use crate::parse::LexerWrapper;
use crate::token::{Extra, Tag};

pub trait Combinator: Sized {
    type Item;

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item>;
}

impl<A: Combinator, B: Combinator> Combinator for (A, B) {
    type Item = (A::Item, B::Item);

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        let a = self.0.parse(src)?;
        let b = self.1.parse(src)?;
        Some((a, b))
    }
}

impl<A: Combinator, B: Combinator, C: Combinator> Combinator for (A, B, C) {
    type Item = (A::Item, B::Item, C::Item);

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        let a = self.0.parse(src)?;
        let b = self.1.parse(src)?;
        let c = self.2.parse(src)?;
        Some((a, b, c))
    }
}

// not TODO combinators for more tuples

pub struct Map<T, U, F: Fn(T) -> U, C: Combinator<Item = T>>(C, F);

impl<T, U, F: Fn(T) -> U, C: Combinator<Item = T>> Combinator for Map<T, U, F, C> {
    type Item = U;

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        self.0.parse(src).map(&self.1)
    }
}

pub struct Star<T: Combinator>(pub T);

impl<T: Combinator> Combinator for Star<T> {
    type Item = Vec<T::Item>;

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        let mut r = Vec::new();

        while let Some(i) = self.0.parse(src) {
            r.push(i);
        }

        Some(r)
    }
}

pub struct Separated<S: Combinator, T: Combinator>(pub S, pub T);

impl<S: Combinator, T: Combinator> Combinator for Separated<S, T> {
    type Item = Vec<T::Item>;

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        let mut r = Vec::new();

        if let Some(i) = self.1.parse(src) {
            r.push(i);

            while let Some(_) = self.0.parse(src) {
                r.push(self.1.parse(src)?);
            }
        }

        Some(r)
    }
}

pub struct Literal(pub Tag);

impl Combinator for Literal {
    type Item = (Tag, Option<Extra>);

    fn parse<'a>(&self, src: &mut LexerWrapper<'a>) -> Option<Self::Item> {
        let t = src.expect(self.0).ok()?;
        Some((t.tag, t.extra))
    }
}
