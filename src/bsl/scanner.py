#!/usr/bin/env python3
from typing import List
from .token_type import TokenType
from .bsl_token import BslToken
from fractions import Fraction
import re
from .numbers import ScientificNotation
from .numbers import Complex
from .regular_expressions import REAL, FRACTION, EXACT_REAL

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
        self.had_error = False

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

                # resulting text is either identifier or number literal
                text = self.source[self.start: self.current]

                if (self.is_number_literal(text)):
                    self.add_literal_token(TokenType.NUMBER, text)
                    return

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
                self.tokens.append(
                    BslToken(type, text, Complex(text), self.line))
            elif self.is_scientific_notation(text):
                self.tokens.append(
                    BslToken(type, text, ScientificNotation(text), self.line))
            else:
                self.tokens.append(
                    BslToken(type, text, Fraction(text), self.line))
            return

        self.tokens.append(BslToken(type, text, literal, self.line))

    def string(self):
        """Obtain the string starting from the scanner's current position."""

        literal = ""
        while not self.is_at_end():
            if self.peek() == '\\':
                self.advance()
                escaped_char = self.peek()
                # for info on BSL escape sequences, see 
                # https://docs.racket-lang.org/reference/reader.html#(part._parse-string)
                match escaped_char:
                    case 'a':
                        literal += '\a'
                    case 'b':
                        literal += '\b'
                    case 't':
                        literal += '\t' 
                    case 'n':
                        literal += '\n'
                    case 'v':
                        literal += '\v'
                    case 'f':
                        literal += '\f'
                    case 'r':
                        literal += '\r'
                    case 'e':
                        literal += '\x1b'
                    case '\'':
                        literal += '\''
                    case '"':
                        literal += '"'
                    case 'n':
                        literal += '\n'
                    # \<digit>{1,3} -> unicode octal number 1-3 digits
                    case escaped_char if self.is_octal(escaped_char):
                        literal += self.decode_numeric_escape(8, 3)
                        continue 
                    # \x<digit>{1,2} -> unicode hex number 1-2 digits
                    case "x":
                        self.advance()
                        literal += self.decode_numeric_escape(16, 2)
                        continue
                    # \u<digit>{1,4} or surrogate pair u\<digit>{4,4}u\<digit>{4,4}
                    # https://en.wikipedia.org/wiki/UTF-16#U+D800_to_U+DFFF_(surrogates)
                    # UTF-16 surrogate pair:
                    # high in D800-DBFF, low in DC00-DFFF
                    # codepoint = 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
                    case "u":
                        self.advance()
                        high_surrogate = self.decode_numeric_escape(16, 4)
                        high_surrogate_hex = ord(high_surrogate)
                        
                        # check if value is a valid high surrogate
                        if not (0xD800 <= high_surrogate_hex <= 0xDBFF):
                            literal += high_surrogate
                            continue

                        # if we get a high surrogate there MUST be a low surrogate DIRECTLY AFTER IT
                        # that is also a hex number unicode hex number of 4 digits. 
                        # otherwise, it's an error. Yes, this is how Racket/BSL does things.
                        if not self.peek() == '\\':
                            self.report_surrogate_error(high_surrogate)
                            return
                        self.advance()
                        if not self.peek() == 'u':
                            self.report_surrogate_error(high_surrogate)
                            return
                        self.advance()

                        low_surrogate = self.decode_numeric_escape(16, 4)
                        low_surrogate_hex = ord(low_surrogate)
                        # check if low surrogate is valid
                        if not (0xDC00 <= low_surrogate_hex <= 0xDFFF):
                            self.report_surrogate_error(high_surrogate + low_surrogate)
                            return
                        literal += chr(0x10000 + ((high_surrogate_hex - 0xD800) << 10) + (low_surrogate_hex - 0xDC00))
                        continue
                    # \<digit>{1,8} -> unicode hex number 1-8 digits
                    case "U":
                        self.advance()
                        literal += self.decode_numeric_escape(16, 8)
                        continue
                    case _:
                        self.error_reporter.error(self.line, "Invalid escape sequence.")
                        return
                self.advance()
                continue
            elif self.peek() == '"':
                break
            elif self.peek() == '\n':
                self.line += 1
            
            literal += self.peek()
            self.advance()

        if self.is_at_end():
            self.error_reporter.error(self.line, "Unterminated string.")
            return

        # advance to go past the closing double quote
        self.advance()

        self.add_literal_token(TokenType.STRING, literal)

    def is_number_literal(self, text):
        """Check if some text is a number."""

        return (self.is_real_number(text) or
                self.is_fraction(text) or
                self.is_scientific_notation(text) or
                self.is_complex_number(text))

    def is_hex(self, text):
        """Check if some text is a valid hex number."""
        return re.fullmatch(r"^[0-9a-fA-F]+$", text or "") is not None 

    def is_octal(self, text):
        """Check if some text is a valid octal number."""
        return re.fullmatch(r"^[0-7]+$", text or "") is not None 

    def is_real_number(self, text):
        """Check if some text is a decimal number."""
        return re.fullmatch(f"^[+-]?{REAL}$", text, re.VERBOSE) is not None

    def is_fraction(self, text) -> bool:
        """Check if some text is a fraction number."""
        return re.fullmatch(rf"^[+-]?{FRACTION}$", text) is not None

    def is_scientific_notation(self, text) -> bool:
        """Check if some text is a scientific notation number."""
        return re.fullmatch(r"[0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+", text) is not None

    def is_complex_number(self, text) -> bool:
        """Return true if text is a valid complex number."""
        return re.fullmatch(rf"([+-]?{EXACT_REAL})([+-]{EXACT_REAL})i", text) is not None
    
    def report_surrogate_error(self, literal: str) -> None:
        """Report a surrogate error."""
        self.error_reporter.error(
            self.line,
            "read-syntax: bad or incomplete surrogate-style encoding at `{literal}`")

    def decode_numeric_escape(self, base: int, max_digits: int) -> chr:
        """Decode a numeric escape sequence."""
        hex_number = ""
        for _ in range(max_digits):
            if self.is_at_end() or not self.is_hex(self.peek()):
                break
            hex_number += self.peek()
            self.advance()
        return chr(int(hex_number, base)) if hex_number else ""

    def boolean(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start: self.current]

        if text == "#true":
            self.add_literal_token(TokenType.BOOLEAN, True)
        elif text == "#false":
            self.add_literal_token(TokenType.BOOLEAN, False)
        else:
            self.error_reporter.error(
                self.line,
                "identifiers cannot start with '#'")

    def is_valid_id_char(self, c):
        """Check if a character is a valid identifier character."""
        return (not c.isspace()) and (c not in '",\'`()[]{}|;#')

    def peek(self):
        """Look one character ahead without consuming the character."""
        return self.source[self.current] if not self.is_at_end() else '\0'

    def match(self, expected: str) -> bool:
        """Match the next character in the current scanner's position."""
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    


if __name__ == '__main__':
    print("start")
    from .error_reporter import ErrorReporter

    # print("""  "\\""  """)
    scanner = Scanner(""" 
    "\\a"
    "\\b"
    "\\t"
    "\\n"                 
    "\\v"
    "\\f"
    "\\r"
    "\\e"
    "\\'"
    "\\""
    "\\n"
    """,
    ErrorReporter())

    scanner.scan_tokens()

    for token in scanner.tokens:
        print(f"token: {token.to_string()}")

    print("end")
