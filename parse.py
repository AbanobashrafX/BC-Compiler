import sys
from lex import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        # Call nextToken() twice to initialize current and peek.
        self.currentToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    def checkToken(self, kind):
        # Return true if the current token matches.
        return kind == self.currentToken.kind

    def checkPeek(self, kind):
        # Return true if the next token matches.
        return kind == self.peekToken.kind

    def match(self, kind):
        # Try to match current token.
        # If not, error. Advances the current token.
        if not self.checkToken(kind):
            self.abort(f"[!] Expected: {kind}")
        self.nextToken()

    def nextToken(self):
        # Advances the current token.
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    @staticmethod
    def abort(message):
        sys.exit(f"[Error parsing] {message}")

    def statement(self):
        # Check the first token to see what kind of statement this is.
        if self.checkToken(TokenType.PRINT):
            print("[+] PRINT STATEMENT")
            self.nextToken()
            # "PRINT" (expression | string)
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("[+] IF STATEMENT")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("[+] WHILE STATEMENT")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # Zero or more statements in the loop body.
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("[+] LABEL STATEMENT")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("[+] GOTO STATEMENT")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("[+] LET STATEMENT")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("[+] INPUT STATEMENT")
            self.nextToken()
            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.currentToken.text + " (" + self.currentToken.kind.name + ")")

        # Newline.
        self.nl()

    def nl(self):
        print("[+] NEWLINE")

        nlToken = TokenType.NEWLINE
        self.match(nlToken)     # Require at least one newline.

        while self.checkToken(nlToken):
            self.nextToken()

    def program(self):
        print("=== PROGRAM ===")
        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()
