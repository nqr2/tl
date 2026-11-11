pub struct Receiver {
    pub name: String,
    pub ty: Box<Type>,
}

pub enum Message {
    Unary(String),

    Binary {
        message: String,
        rhs: Box<Expression>,
    },

    Keyword {
        message: Vec<String>,
        arguments: Vec<String>,
    },
}

pub enum MessageName {
    Unary(String),
    Binary(String),
    Keyword(Vec<String>),
}

pub enum Expression {
    Pass,

    Break {
        label: String,
        value: Box<Expression>,
    },

    Cascade {
        receiver: Box<Expression>,
        message: Message,
    },

    Send {
        receiver: Box<Expression>,
        message: Message,
    },
}

pub struct Member {
    pub name: String,
    pub ty: Box<Type>,
}

pub struct TyCase {
    pub message: MessageName,
    pub arguments: Vec<Type>,
}

pub enum Type {
    Pass,

    Named(String),

    Function {
        arguments: Vec<Type>,
        ret: Box<Type>,
    },

    Pointer {
        mutable: bool,
        item: Box<Type>,
    },

    Array {
        length: usize,
        item: Box<Type>,
    },

    Struct(Vec<Member>),

    Match(Vec<TyCase>),
}
