#!/usr/bin/env python3
from typing import List
from .token_type import TokenType
from .bsl_token import BslToken


class Scanner:
    """Create Object to scan source code."""

    def __init__(self, source: str, error_reporter: object):
        """
        Initialize the scanner by passing source code.
        Token list is initialized automatically.
        """
        self.source = source
        self.tokens: List[BslToken] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_reporter = error_reporter

    def scan_tokens(self):
        """Start a scan on the source code given to the Scanner."""
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(BslToken(TokenType.EOF, "", None, self.line))

    def is_at_end(self) -> bool:
        """Check if scanner is at the end of source."""
        return self.current >= len(self.source)

    def scan_token(self):
        """Scan the current token and add it to token list."""
        c = self.advance()
        match c:
            case '(':
                self.add_non_literal_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_non_literal_token(TokenType.RIGHT_PAREN)
            case '[':
                self.add_non_literal_token(TokenType.LEFT_BRACK)
            case ']':
                self.add_non_literal_token(TokenType.RIGHT_BRACK)
            case '{':
                self.add_non_literal_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_non_literal_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_non_literal_token(TokenType.COMMA)
            case ';':
                self.add_non_literal_token(TokenType.SEMICOLON)
            case '`':
                self.add_non_literal_token(TokenType.BACK_TICK)
            case '"':
                self.string()
            case '\n':
                self.line += 1
            case ' ' | '\r' | '\t':
                pass
            case '#':
                self.boolean()
            case _:
                while ((not self.is_at_end()) and
                       self.is_valid_id_char(self.peek())):
                    self.advance()

                text = self.source[self.start: self.current]

                is_number_literal = self.is_number_literal(text)

                if is_number_literal:
                    self.add_literal_token(TokenType.NUMBER, float(text))
                elif not is_number_literal:
                    self.add_non_literal_token(TokenType.IDENTIFIER)

                # self.error_reporter.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        """Advance the scanner and return the consumed chararacter."""
        consumed_character = self.source[self.current]

        self.current += 1
        return consumed_character

    def add_non_literal_token(self, type: TokenType):
        """Add a non-literal token given a TokenType and."""
        self.add_literal_token(type, None)

    def add_literal_token(self, type: TokenType, literal: object):
        """Add a token for a literal given a TokenType and a literal object."""
        text = self.source[self.start: self.current]
        self.tokens.append(BslToken(type, text, literal, self.line))

    def string(self):
        """Obtain the string starting from the scanner's current position."""
        while (self.peek() != '"' and (not self.is_at_end())):
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error_reporter.error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1: self.current - 1]

        self.add_literal_token(TokenType.STRING, value)

    def is_number_literal(self, text):
        """Check a if some text is a number."""
        # check if text is a number
        seen_dot = False

        for char in text:
            if char.isdigit():
                continue
            elif char == "." and not seen_dot:
                seen_dot = True
            else:
                return False
        return True

    def boolean(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start: self.current]

        if text == "#true":
            self.add_literal_token(TokenType.BOOLEAN, text)
        elif text == "#false":
            self.add_literal_token(TokenType.BOOLEAN, text)
        else:
            self.error_reporter.error(
                self.line,
                "identifiers cannot start with '#'")

    def is_valid_id_char(self, c):
        return (not c.isspace()) and (c not in '",\'`()[]{}|;#')

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
    print("start")
    from .error_reporter import ErrorReporter

    error_reporter = ErrorReporter()
    scanner = Scanner("(){}[],#;`\"bruh\"\n123 bruh", error_reporter)
    scanner.scan_tokens()

    for token in scanner.tokens:
        print(f"token: {token.to_string()}")
    print("end")
