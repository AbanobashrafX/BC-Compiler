from lex import Lexer, TokenType


class Compiler:

    @staticmethod
    def test_lexer():
        source = "LET num = 123"
        lexer = Lexer(source)

        while lexer.peek() != "\0":
            print(lexer.curChar)
            lexer.nextChar()


if __name__ == "__main__":
    """A small BASIC-to-C compiler"""
    c = Compiler()
    c.test_lexer()
