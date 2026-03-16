#!/usr/bin/env python3
from bsl.token_type import TokenType
from bsl.error_reporter import ErrorReporter
from bsl.scanner import Scanner
from bsl.bsl_token import BslToken
import pytest


# @pytest.fixture
def test_scanner():
    scanner = Scanner("() ) {} } \n [] ]", ErrorReporter())
    scanner.scan_tokens()

    # Uses decorator to allow for equality.
    assert scanner.tokens == [
        BslToken(TokenType.LEFT_PAREN, '(', None, 1),
        BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
        BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
        BslToken(TokenType.LEFT_BRACE, '{', None, 1),
        BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
        BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
        BslToken(TokenType.LEFT_BRACK, '[', None, 2),
        BslToken(TokenType.RIGHT_BRACK, ']', None, 2),
        BslToken(TokenType.RIGHT_BRACK, ']', None, 2),
        BslToken(TokenType.EOF, "", None, 2)]


# @pytest.fixture
def test_string():
    """Run a test on scanner's ability to lex strings."""
    scanner = Scanner("""
    \"bruh\" \n
    \"1234567890-=!@#$%^&*()_+qwertyuiop
    []asdfghjkl;'zxcvbnm,./{}|:<>?\" \n
    ""
    "\\n"
    "\""
    """,
    ErrorReporter())

    scanner.scan_tokens()

    assert scanner.tokens == [
        BslToken(TokenType.STRING, '"bruh"', "bruh", 1),
        BslToken(TokenType.STRING,
                 '"1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;\'zxcvbnm,./{}|:<>?"',
                 "1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;'zxcvbnm,./{}|:<>?", 2),
        BslToken(TokenType.STRING, '""', '', 3),
        BslToken(TokenType.STRING, '"\\n"', "\\n", 3),
        BslToken(TokenType.STRING, '"\""', "\"", 3),
        BslToken(TokenType.EOF, "", None, 3),
    ]


def test_decimal_numbers():
    """Run a test on all the scanners ability to lex numbers."""
    scanner = Scanner("""
    1\n
    123412345678908765432234567890    \n
    1.0\n
    12034029384.12348230943\n
    .12\n
    0.12\n
    000.12\n
    """,
    ErrorReporter())

    scanner.scan_tokens()

    assert scanner.tokens == [
        BslToken(TokenType.NUMBER, '1', 1, 1),
        BslToken(TokenType.NUMBER,
                 '123412345678908765432234567890',
                 123412345678908765432234567890,
                 2),
        BslToken(TokenType.NUMBER, "1.0", 1.0, 3),
        BslToken(TokenType.NUMBER,
                 "12034029384.12348230943",
                 12034029384.12348230943,
                 4),
        BslToken(TokenType.NUMBER, ".12", 0.12, 5),
        BslToken(TokenType.NUMBER, "0.12", 0.12, 6),
        BslToken(TokenType.NUMBER, "000.12", 0.12, 6),
        BslToken(TokenType.EOF, "", None, 7)
    ]


def test_rational_numbers():
    """Run a test on scanner's ability to lex strings."""
    scanner = Scanner("""
    1/2
    """,
    ErrorReporter())

    for token in scanner.tokens:
        print(f"token: {token.to_string()}")
    print("end")

    pass


def test_scientific_notation():
    pass


def text_complex_numbers():
    pass

# def test_number_error():
#     """Run a test on all the scanners ability to lex numbers."""
#     scanner = Scanner("""
#     123.123.123.123.123
#     """,
#     ErrorReporter())

# if __name__ == '__main__':
#     print("start")
#     from .error_reporter import ErrorReporter

#     error_reporter = ErrorReporter()
#     scanner = Scanner("(){}[],#;`\"bruh\"\n123 bruh", error_reporter)
#     scanner.scan_tokens()

#     for token in scanner.tokens:
#         print(f"token: {token.to_string()}")
#     print("end")

    #     scanner.scan_tokens()
    # def test_number(self):


# if  __name__ == '__main__':
#     unittest.main()
