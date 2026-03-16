#!/usr/bin/env python3
from typing import List
from .token_type import TokenType
from .bsl_token import BslToken
from fractions import Fraction
from decimal import Decimal
import re

REAL = r"(?:\d+(?:\.\d*)?|\.\d+)"

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

                if (self.is_number_literal(text)):
                    self.add_literal_token(TokenType.NUMBER, text)
                    return

                # if previous try blocks didn't work. Then text is identifier
                self.add_non_literal_token(TokenType.IDENTIFIER)

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

        if type == TokenType.NUMBER:
            if self.is_complex_number(text):
                text_replaced_j = text.replace("i", "j")
                self.tokens.append(
                    BslToken(type, text, Complex(text_replaced_j), self.line))
            else:
                self.tokens.append(
                    BslToken(type, text, Fraction(text), self.line))
            return

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
        """Check if some text is a number."""

        if (self.is_real_number(text)):
            return True
        elif (self.is_fraction(text)):
            return True
        elif (self.is_scientific_notation(text)):
            return True
        elif (self.is_complex_number(text)):
            return True
        else:
            return False

    def is_real_number(self, text):
        """Check if some text is a decimal number."""

        real_number = re.fullmatch(f"^{REAL}$", text, re.VERBOSE)

        print(f"real_number: {real_number}")

        if real_number is None:
            return False
        else:
            return True

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

    def is_fraction(self, text) -> bool:
        """Check if some text is a fraction number."""
        fraction = re.fullmatch(r"^[+-]?(\d+)/(\d+)$", text)

        # print(f"fraction: {fraction}")
        if fraction is None:
            return False
        else:
            True

        slash_index = text.find("/")
        if (slash_index == -1):
            return False

        numerator = text[:slash_index]

        if not numerator.isdigit():
            return False
        else:
            numerator = int(numerator)

        denominator_index = slash_index + 1
        denominator = text[denominator_index:]

        if not denominator.isdigit():
            return False
        else:
            denominator = int(denominator)

        return True

    def is_scientific_notation(self, text) -> bool:
        """
        Attempt to parse number using scientific notation.
        Note that scientific notation counts as float in Python.
        """
        scientific_notation = re.fullmatch(r"[0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+", text)
        # print(f"scientific_notation: {scientific_notation}")
        if scientific_notation is None:
            return False
        else:
            return True

        e_index = text.find("e")
        if (e_index == -1):
            return False

        coefficient = text[:e_index]

        if not self.is_real_number(text):
            return False

        exponent_index = e_index + 1
        coefficient = text[exponent_index]

        if not coefficient.isdigit():
            return False

        return True

    def is_complex_number(self, text) -> bool:
        """Return true if text is a valid complex number."""

        complex_number = re.fullmatch(rf"^[+-]?{REAL}[+-]{REAL}i$", text)

        if complex_number is None:
            return False
        else:
            return True

        plus_index = text.find("+")
        if (plus_index == -1):
            return False

        real_number = text[:plus_index]

        if not self.is_real_number(real_number) and not self.is_fraction(real_number):
            return False

        # last character must be i
        if (text[len(text) - 1] != "i"):
            return False

        before_i_index = len(text) - 1
        after_plus_index = plus_index + 1
        second_real = text[after_plus_index: before_i_index]

        if not self.is_real_number(second_real) and not self.is_fraction(second_real):
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

# Complex object for literal, internal representation of value.
class Complex:
    def __init__(self, real_part: Fraction, imaginary_part: Fraction):
        self.real_part = real_part
        self.imaginary_part = imaginary_part

    def to_string(self) -> str:
        """Get the human-readable string representation of complex number."""
        return f"{self.real_part}+{self.imaginary_part}i"



if __name__ == '__main__':
    print("start")
    from .error_reporter import ErrorReporter

    error_reporter = ErrorReporter()
    scanner = Scanner("0.12 1/2 1.2e10 -.2+.2i", error_reporter)
    scanner.scan_tokens()

    for token in scanner.tokens:
        print(f"token: {token.to_string()}")
    print("end")
