from sys import exit
from tokens import Token, TokenType


class Lexer:
    """
    The first module of our compiler is called the lexer.
    Given a string of Teeny Tiny code, it will iterate 
    character by character to do two things: decide 
    where each token starts/stops and what type of token it is.
    If the lexer is unable to do this, then it will report an error
    for an invalid token.
    """

    def __init__(self, code):
        # Source code to lex as a string.
        # Append a newline to simplify lexing/parsing the last token/statement.
        self.source = code + "\n"
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        """
        This increments the lexer current position and updates the current character.
        If we reach the end of the input, set the character to the end-of-file marker.
        This is the only place we will modify curPos and curChar.
        But sometimes we want to look ahead to the next character without updating curPos:
        """
        return "\0" if self.curPos + 1 >= len(self.source) else self.source[self.curPos + 1]

    # Invalid token found, print error message and exit.
    @staticmethod
    def abort(message):
        exit(f"[Lexing error] {message}")

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar in [" ", "\t", "\r"]:
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token.
    def getToken(self):
        """
        Check the first character of this token to see if we can decide what it is.
        If it is a multiple character operator (e.g., !=), number, identifier, or keyword 
        then we will process the rest.        
        """
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            if self.peek() == "*":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.POW)
            else:
                token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "=":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        else:
            self.abort(f"Unknown token: {self.curChar}")

        self.nextChar()
        return token
