#[derive(PartialEq, Eq)]
pub enum Tag {
    Eof,        // <end of file>
    Identifier, // <identifier>
    Keyword,    // identifier:
    Operator,   // <operator>
    LParen,     // (
    RParen,     // )
    LBrac,      // [
    RBrac,      // ]
    Comment,    // "comment..."
    Equal,      // =
    Arrow,      // ->
    LCurl,      // {
    RCurl,      // }
    Hash,       // #
    Comma,      // ,
    At,         // @
    Semicolon,  // ;
    Colon,      // :
    Dot,        // .
    String,     // 'string...'
    Char,       // `c`
    Int,        // <integer>
    Float,      // <float>
    Module,     // module
    Import,     // import
    Type,       // type
    Var,        // var
    Const,      // const
    Match,      // match
    With,       // with
    Set,        // set
    Label,      // label
    Break,      // break
    And,        // and
    Then,       // then
    As,         // as
    Pass,       // pass
    Fn,         // fn
    Decl,       // decl
    Extends,    // extends
}

pub struct Token<'a> {
    pub tag: Tag,
    pub span: (usize, usize),
    pub slice: &'a str,
}
