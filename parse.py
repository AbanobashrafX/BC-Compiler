import sys
from lex import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()            # Variables declared so far.
        self.labelsDeclared = set()     # Labels declared so far.
        self.labelsGoto = set()         # Labels gotonext so far.

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

        # "WHILE" comparison "REPEAT" {statement} "END-WHILE"
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

            # Make sure this label doesn't already exist.
            if self.currentToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.currentToken.text)
            self.labelsDeclared.add(self.currentToken.text)

            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("[+] GOTO STATEMENT")
            self.nextToken()
            self.labelsGoto.add(self.currentToken.text)
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("[+] LET STATEMENT")
            self.nextToken()

            #  Check if ident exists in symbol table. If not, declare it.
            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("[+] INPUT STATEMENT")
            self.nextToken()

            # If variable doesn't already exist, declare it.
            if self.currentToken.text not in self.symbols:
                self.symbols.add(self.currentToken.text)

            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.currentToken.text + " (" + self.currentToken.kind.name + ")")

        # Newline.
        self.nl()

    def isComparisonOperator(self):
        # Return true if the current token is a comparison operator.
        operators = [TokenType.GT, TokenType.GTEQ, TokenType.LT, TokenType.LTEQ, TokenType.EQEQ, TokenType.NOTEQ]
        return any(self.checkToken(op) for op in operators)

    def primary(self):
        print("[+] PRIMARY (" + self.currentToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists.
            if self.currentToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.currentToken.text)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.currentToken.text)     # Error!

    def unary(self):
        print("[+] UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def term(self):
        print("[+] TERM")

        self.unary()
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    def expression(self):
        print("[+] EXPRESSION")

        self.term()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    def comparison(self):
        print("[+] COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.currentToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def nl(self):
        print("[+] NEWLINE")

        nlToken = TokenType.NEWLINE
        self.match(nlToken)     # Require at least one newline.

        while self.checkToken(nlToken):
            self.nextToken()

    def program(self):
        print("=== PROGRAM ===")
        # Parse and skip all the newlines in the beginning of the program.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # Check that each label referenced in a GOTO is declared.
        for label in self.labelsGoto:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)
