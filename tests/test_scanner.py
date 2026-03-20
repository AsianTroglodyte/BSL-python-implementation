#!/usr/bin/env python3
from bsl.token_type import TokenType
from bsl.error_reporter import ErrorReporter
from bsl.scanner import Scanner
from bsl.bsl_token import BslToken
from fractions import Fraction
import pytest


def scan_single_lexeme(lexeme: str):
    scanner = Scanner(lexeme, ErrorReporter())
    scanner.scan_tokens()
    # Expect one token + EOF
    assert len(scanner.tokens) == 2
    return scanner.tokens[0]


@pytest.mark.parametrize("lexeme,expected_token", [ 
    ("(", BslToken(TokenType.LEFT_PAREN, "(", None, 1)),
    (")", BslToken(TokenType.RIGHT_PAREN, ")", None, 1)),
    ("{", BslToken(TokenType.LEFT_BRACE, "{", None, 1)),
    ("}", BslToken(TokenType.RIGHT_BRACE, "}", None, 1)),
    ("\n[", BslToken(TokenType.LEFT_BRACK, "[", None, 2)),
    ("\n]", BslToken(TokenType.RIGHT_BRACK, "]", None, 2)),
    (",", BslToken(TokenType.COMMA, ",", None, 1)),
    (";", BslToken(TokenType.SEMICOLON, ";", None, 1)),
    ("`", BslToken(TokenType.BACK_TICK, "`", None, 1)),
    ("#true", BslToken(TokenType.BOOLEAN, "#true", True, 1)),
    ("#false", BslToken(TokenType.BOOLEAN, "#false", False, 1)),
    ("identifier", BslToken(TokenType.IDENTIFIER, "identifier", None, 1)),
    ("123", BslToken(TokenType.NUMBER, "123", Fraction("123"), 1)),
])
def test_single_lexemes(lexeme, expected_token):
    assert scan_single_lexeme(lexeme) == expected_token


print("bruh")

def test_multiple_lexems():
    scanner = Scanner("""
    ( ) ) { } } [ ] ] , ; ` #true #false identifier 123
    """
    , ErrorReporter())

    scanner.scan_tokens()

    assert scanner.tokens == [
        BslToken(TokenType.LEFT_PAREN, "(", None, 2),
        BslToken(TokenType.RIGHT_PAREN, ")", None, 2),
        BslToken(TokenType.RIGHT_PAREN, ")", None, 2),
        BslToken(TokenType.LEFT_BRACE, "{", None, 2),
        BslToken(TokenType.RIGHT_BRACE, "}", None, 2),
        BslToken(TokenType.RIGHT_BRACE, "}", None, 2),
        BslToken(TokenType.LEFT_BRACK, "[", None, 2),
        BslToken(TokenType.RIGHT_BRACK, "]", None, 2),
        BslToken(TokenType.RIGHT_BRACK, "]", None, 2),
        BslToken(TokenType.COMMA, ",", None, 2),
        BslToken(TokenType.SEMICOLON, ";", None, 2),
        BslToken(TokenType.BACK_TICK, "`", None, 2),
        BslToken(TokenType.BOOLEAN, "#true", True, 2),
        BslToken(TokenType.BOOLEAN, "#false", False, 2),
        BslToken(TokenType.IDENTIFIER, "identifier", None, 2),
        BslToken(TokenType.NUMBER, "123", Fraction("123"), 2),
        BslToken(TokenType.EOF, "", None, 3)
    ]



# @pytest.fixture
def test_string():
    """Run a test on scanner's ability to lex strings."""
    scanner = Scanner(""" "bruh"
    "1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;'zxcvbnm,./{}|:<>?"
    ""
    "y"
    "\\""
    """,
    ErrorReporter())

    scanner.scan_tokens()
    print(scanner.tokens)

    # NOTE: line number for multiline strings is where string ends

    assert scanner.tokens == [
        BslToken(TokenType.STRING, '"bruh"', "bruh", 1),
        BslToken(TokenType.STRING,
                 '"1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;\'zxcvbnm,./{}|:<>?"',
                 "1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;'zxcvbnm,./{}|:<>?", 3),
        BslToken(TokenType.STRING, '""', '', 4),
        BslToken(TokenType.STRING, '"y"', "y", 5),
        BslToken(TokenType.STRING, '"\\""', "\"", 6),
        BslToken(TokenType.EOF, "", None, 7),
    ]


# @pytest.mark.parametrize("lexeme, expected_token")
# def test_string_escapes():
#     """Run a test on scanner's ability to lex strings."""
#     scanner = Scanner(""" 
#     "\\a"
#     "\\b"
#     "\\t"
#     "\\n"                 
#     "\\v"
#     "\\f"
#     "\\r"
#     "\\e"
#     "\\'"
#     "\\""
#     "\\n"
#     """,
#     ErrorReporter())

#     scanner.scan_tokens()

#     # NOTE: line number for multiline strings is where string ends

#     assert scanner.tokens == [
#         BslToken(TokenType.STRING, '"bruh"', "bruh", 1),
#         BslToken(TokenType.STRING,
#                  '"1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;\'zxcvbnm,./{}|:<>?"',
#                  "1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;'zxcvbnm,./{}|:<>?", 3),
#         BslToken(TokenType.STRING, '""', '', 4),
#         BslToken(TokenType.STRING, '"y"', "y", 5),
#         BslToken(TokenType.STRING, '"\\""', "\"", 6),
#         BslToken(TokenType.EOF, "", None, 7),
#     ]



# def test_integers():
#     """Run a test on all the scanners ability to lex numbers."""
#     scanner = Scanner("""1
#     123412345678908765432234567890
#     -12
#     +12
#     """,
#     ErrorReporter())

#     scanner.scan_tokens()

#     assert scanner.tokens == [
#         BslToken(TokenType.NUMBER, '1', Fraction(1), 1),
#         BslToken(TokenType.NUMBER,
#                  '123412345678908765432234567890',
#                  123412345678908765432234567890,
#                  2),
#         BslToken(TokenType.NUMBER, '-12', Fraction(-12), 3),
#         BslToken(TokenType.NUMBER, '+12', Fraction(+12), 4),
#         BslToken(TokenType.EOF, "", None, 5)
#     ]


# def test_fractions():
#     """Run a test on scanner's ability to lex strings."""
#     scanner = Scanner("""1/2
#     -1/2
#     -1/-2
#     -1/+2
#     +1/+2
#     123239438/123432488
#     """,
#     ErrorReporter())

#     scanner.scan_tokens()

#     assert scanner.tokens == [
#         BslToken(TokenType.NUMBER, '1/2', Fraction(1, 2), 1),
#         BslToken(TokenType.NUMBER, '-1/2', Fraction(-1, 2), 2),
#         BslToken(TokenType.IDENTIFIER, '-1/-2', None, 3),
#         BslToken(TokenType.IDENTIFIER, '-1/+2', None, 4),
#         BslToken(TokenType.IDENTIFIER, '+1/+2', None, 5),
#         BslToken(TokenType.NUMBER,
#                  '123239438/123432488',
#                  Fraction(123239438, 123432488),
#                  6),
#         BslToken(TokenType.EOF, '', None, 7),
#     ]


# @pytest.mark.parametrize( "lexeme,expected_literal", [
#     ("1e4", Fraction("1e4")),
#     ("10e-4", Fraction("10e-4")),
#     ("1.23e4", Fraction("1.23e4")),
#     ("1.23e-4", Fraction("1.23e-4")),
#     ("1.23E+4", Fraction("1.23E+4")),
# ])
# def test_scientific_notation_valid(lexeme, expected_literal):
#     token = scan_single_lexeme(lexeme)
#     assert token.token_type == TokenType.NUMBER
#     assert token.lexeme == lexeme
#     assert token.literal == expected_literal


# @pytest.mark.parametrize(
#     "lexeme",
#     [
#         "e10",      # missing coefficient
#         "1e",       # missing exponent digits
#         "1e+",      # sign but no exponent digits
#         "1.e4",     # dot without trailing digits (by current regex)
#         ".5e4",     # leading dot form not allowed by current regex
#         "-1e4",     # not allowed by current scientific regex
#         "+1e4",     # not allowed by current scientific regex
#         "1/2e4",    # rational scientific not supported currently
#         "1/2e-1/2", # invalid exponent
#         "1/23e0.5", # exponent not integer
#     ],
# )
# def test_scientific_notation_invalid(lexeme):
#     token = scan_single_lexeme(lexeme)
#     assert token.token_type == TokenType.IDENTIFIER
#     assert token.lexeme == lexeme
#     assert token.literal is None


# def text_complex_numbers():

#     pass

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
