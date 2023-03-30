import sys

from lex import Lexer, TokenType
from parse import *


class Compiler:
    """
    TODO: Our own Teeny Tiny programming language.
    The compiler will work in three stages:
        (1) lexing, which breaks the input code up into small pieces called tokens,
        (2) parsing, which verifies that the tokens are in an order that our language allows, and
        (3) emitting, which produces the appropriate C code.
    """

    @staticmethod
    def test_lexer():
        print("=== Lexer ===")

        source = "LET num = 123"
        lexer = Lexer(source)

        while lexer.peek() != "\0":
            print(lexer.curChar)
            lexer.nextChar()

    @staticmethod
    def test_token():
        print("=== Token ===")

        source = """
        IF 2*2 == 4 THEN PRINT TRUE ENDIF
        # This is a comment! 
        PRINT E=mc**2
        """
        lexer = Lexer(source)
        token = lexer.getToken()

        while token.kind != TokenType.EOF:
            print(token.kind)
            token = lexer.getToken()

    @staticmethod
    def test_parsing():
        print("=== Parser  ===")

        # if len(sys.argv) != 2:
        #     sys.exit("Error: compiler needs source file as argument.")
        # with open(sys.argv[1], "r") as codeFile:
        #     source = codeFile.read()
        with open('example/hello.code', "r") as codeFile:
            source = codeFile.read()

        # Initialize the lexer and parser.
        lexer = Lexer(source)
        parser = Parser(lexer)

        # Start the program
        parser.program()
        print("=== End ===")


if __name__ == "__main__":
    """A small BASIC-to-C compiler"""
    c = Compiler()
    c.test_parsing()
