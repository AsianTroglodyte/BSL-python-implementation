#!/usr/bin/env python3
from typing import List
from token import Token
from token_type import TokenType


class Scanner:
    """Create Object to scan source code."""

    def __init__(self, source: str, error_reporter: object):
        """
        Initialize the scanner by passing source code.
        Token list is initialized automatically.
        """
        self.source = source
        self.tokens: List(Token) = []
        self.start = 0
        self.current = 0
        self.line = 0
        self.error_reporter = error_reporter

    def scan_tokens(self):
        """Start a scan on the source code given to the Scanner."""
        while not (self.is_at_end()):
            self.start = self.current
            self.scan_token()
            print("after scan_token()")

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

    def is_at_end(self) -> bool:
        """Check if scanner is at the end of source."""
        return self.current >= len(self.source)

    def scan_token(self):
        """Scan the current token and add it to token list."""
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN, c)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN, c)
            case '[':
                self.add_token(TokenType.LEFT_BRACK, c)
            case ']':
                self.add_token(TokenType.RIGHT_BRACK, c)
            case '{':
                self.add_token(TokenType.RIGHT_BRACE, c)
            case '}':
                self.add_token(TokenType.LEFT_BRACE, c)
            case ',':
                self.add_token(TokenType.COMMA, c)
            case '#':
                self.add_token(TokenType.POUND, c)
            case ';':
                self.add_token(TokenType.SEMICOLON, c)
            case '`':
                self.add_token(TokenType.BACK_TICK, c)
            case '"':
                self.string()
            # case '\n':
            #     self.line += 1
            # case " ":
            #     return
            # case _:
            #     self.error_reporter.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        """Advance the scanner and return the consumed chararacter."""
        consumed_character = self.source[self.current]
        print(f"consumed_character {consumed_character}")
        self.current += 1
        return consumed_character

    def add_token(self, type: TokenType, literal: object):
        """Add a token given a TokenType and literal object."""
        text = self.source[self.start: self.current]
        self.tokens.append(Token(type, text, literal, self.line))
        print("add_token")

    def string(self):
        """Obtain the string starting from the scanner's current position."""
        while not (self.peek() != '"' and (not self.is_at_end())):
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error_reporter.error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start: self.current]

        return value

    def peek(self):
        """Look one character ahead without consuming the character."""
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def match(self, expected: str) -> bool:
        """Match the next character in the current scanner's position."""
        if self.is_at_end():
            return False
        if (self.source[self.current] != expected):
            return False

        self.current += 1
        return True


if __name__ == '__main__':
    from error_reporter import ErrorReporter

    error_reporter = ErrorReporter()
    scanner = Scanner("(){}[],#;`\"bruh\"", error_reporter)
    scanner.scan_tokens()

    # for token in scanner.tokens:
    #     print(f"token: {token.to_string()}")
    # print("bruh2")
