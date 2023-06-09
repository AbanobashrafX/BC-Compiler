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
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort(f"[Expected] !=, got ! {self.peek()}")
        elif self.curChar == '\"':
            """
                1 - Get characters between quotations.
                2 - Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                : We will be using C's printf on this string.
            """
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                if self.curChar in ["\r", "\n", "\t", "\\", "%"]:
                    self.abort(f"{self.curChar} is Illegal character.")
                self.nextChar()

            # Get the substring.
            tokText = self.source[startPos: self.curPos]
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            # Get the substring.
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alphanumeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            # Get the substring.
            tokText = self.source[startPos: self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword is None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        else:
            self.abort(f"Unknown token: {self.curChar}")

        self.nextChar()
        return token
