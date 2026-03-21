#!/usr/bin/env python3
from bsl.token_type import TokenType
from bsl.error_reporter import ErrorReporter
from bsl.scanner import Scanner
from fractions import Fraction
from bsl.numbers import Complex, ScientificNotation
import pytest


class RecordingErrorReporter:
    """Collect scanner errors without printing (for error-path tests)."""

    def __init__(self) -> None:
        self.errors: list[tuple[int, str]] = []

    def error(self, line: int, message: str) -> None:
        self.errors.append((line, message))

    def report(self, line: int, where: str, message: str) -> None:
        self.errors.append((line, message))


def scan_single_lexeme(lexeme: str):
    scanner = Scanner(lexeme, ErrorReporter())
    scanner.scan_tokens()
    # Expect one token + EOF
    assert len(scanner.tokens) == 2
    return scanner.tokens[0]


@pytest.mark.parametrize("src,token_type,lexeme,object,line", [
    ("(", TokenType.LEFT_PAREN, '(', None, 1),
    (")", TokenType.RIGHT_PAREN, ')', None, 1),
    ("{", TokenType.LEFT_BRACE, '{', None, 1),
    ("}", TokenType.RIGHT_BRACE, '}', None, 1),
    ("[", TokenType.LEFT_BRACK, '[', None, 1),
    ("]", TokenType.RIGHT_BRACK, "]", None, 1),
    (",", TokenType.COMMA, ',', None, 1),
    (";", TokenType.SEMICOLON, ';', None, 1),
    ("`", TokenType.BACK_TICK, '`', None, 1),
    ("#true", TokenType.BOOLEAN, '#true', True, 1),
    ("#false", TokenType.BOOLEAN, '#false', False, 1),
    ("identifier", TokenType.IDENTIFIER, 'identifier', None, 1),
    ("123", TokenType.NUMBER, '123', Fraction("123"), 1),
    ('"strong"', TokenType.STRING, '"strong"', "strong", 1),
])
def test_single_lexemes(src, token_type, lexeme, object, line):
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == token_type
    assert scanner.tokens[0].lexeme == lexeme
    assert scanner.tokens[0].literal == object
    assert scanner.tokens[0].line == line


def test_multiple_lexemes():
    scanner = Scanner("""
    ( ) ) { } } [ ] ] , ; ` #true #false identifier 123
    """, ErrorReporter())

    scanner.scan_tokens()

    expected_tokens = [
        (TokenType.LEFT_PAREN, "(", None, 2),
        (TokenType.RIGHT_PAREN, ")", None, 2),
        (TokenType.RIGHT_PAREN, ")", None, 2),
        (TokenType.LEFT_BRACE, "{", None, 2),
        (TokenType.RIGHT_BRACE, "}", None, 2),
        (TokenType.RIGHT_BRACE, "}", None, 2),
        (TokenType.LEFT_BRACK, "[", None, 2),
        (TokenType.RIGHT_BRACK, "]", None, 2),
        (TokenType.RIGHT_BRACK, "]", None, 2),
        (TokenType.COMMA, ",", None, 2),
        (TokenType.SEMICOLON, ";", None, 2),
        (TokenType.BACK_TICK, "`", None, 2),
        (TokenType.BOOLEAN, "#true", True, 2),
        (TokenType.BOOLEAN, "#false", False, 2),
        (TokenType.IDENTIFIER, "identifier", None, 2),
        (TokenType.NUMBER, "123", Fraction("123"), 2),
        (TokenType.EOF, "", None, 3)
    ]
    actual_tokens = [
        (token.type, token.lexeme, token.literal, token.line)
        for token in scanner.tokens
    ]
    assert actual_tokens == expected_tokens


@pytest.mark.parametrize(
    "src,expected_tokens",
    [
        (
            ')(#true"hi")',
            [
                (TokenType.RIGHT_PAREN, ")", None, 1),
                (TokenType.LEFT_PAREN, "(", None, 1),
                (TokenType.BOOLEAN, "#true", True, 1),
                (TokenType.STRING, '"hi"', "hi", 1),
                (TokenType.RIGHT_PAREN, ")", None, 1),
                (TokenType.EOF, "", None, 1),
            ],
        ),
        (
            "123x",
            [
                (TokenType.IDENTIFIER, "123x", None, 1),
                (TokenType.EOF, "", None, 1),
            ],
        ),
        (
            ')(#true"hi")123',
            [
                (TokenType.RIGHT_PAREN, ")", None, 1),
                (TokenType.LEFT_PAREN, "(", None, 1),
                (TokenType.BOOLEAN, "#true", True, 1),
                (TokenType.STRING, '"hi"', "hi", 1),
                (TokenType.RIGHT_PAREN, ")", None, 1),
                (TokenType.NUMBER, "123", Fraction("123"), 1),
                (TokenType.EOF, "", None, 1),
            ],
        ),
        (
            "true#false",
            [
                (TokenType.IDENTIFIER, "true", None, 1),
                (TokenType.BOOLEAN, "#false", False, 1),
                (TokenType.EOF, "", None, 1),
            ],
        ),
        (
            "foo.bar",
            [
                (TokenType.IDENTIFIER, "foo.bar", None, 1),
                (TokenType.EOF, "", None, 1),
            ],
        ),
    ],
)
def test_abutted_tokens_no_whitespace(src, expected_tokens):
    """Tokens may touch with no spaces; id run is greedy (e.g. 123x is one id)."""
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    actual_tokens = [
        (token.type, token.lexeme, token.literal, token.line)
        for token in scanner.tokens
    ]
    assert actual_tokens == expected_tokens


def test_abutted_scientific_notation_then_paren():
    """Scientific notation lexeme may run to `e` digits; `)` starts next token."""
    scanner = Scanner("1/2e4)", ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.NUMBER
    assert scanner.tokens[0].lexeme == "1/2e4"
    lit = scanner.tokens[0].literal
    assert isinstance(lit, ScientificNotation)
    assert lit.base == Fraction(1, 2)
    assert lit.exponent == 4
    assert scanner.tokens[1].type == TokenType.RIGHT_PAREN
    assert scanner.tokens[2].type == TokenType.EOF


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

    # NOTE: line number for multiline strings is where string ends

    expected_tokens = [
        (TokenType.STRING, '"bruh"', "bruh", 1),
        (TokenType.STRING,
         '"1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;\'zxcvbnm,./{}|:<>?"',
         "1234567890-=!@#$%^&*()_+qwertyuiop[\n]asdfghjkl;'zxcvbnm,./{}|:<>?", 3),
        (TokenType.STRING, '""', '', 4),
        (TokenType.STRING, '"y"', "y", 5),
        (TokenType.STRING, '"\\""', "\"", 6),
        (TokenType.EOF, "", None, 7),
    ]
    actual_tokens = [
        (token.type, token.lexeme, token.literal, token.line)
        for token in scanner.tokens
    ]
    assert actual_tokens == expected_tokens


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    ('"\\a"  ', '"\\a"', '\a'),
    ('"\\b"  ', '"\\b"', '\b'),
    ('"\\t"  ', '"\\t"', '\t'),
    ('"\\n"  ', '"\\n"', '\n'),
    ('"\\v"  ', '"\\v"', '\v'),
    ('"\\f"  ', '"\\f"', '\f'),
    ('"\\r"  ', '"\\r"', '\r'),
    ('"\\e"  ', '"\\e"', '\x1b'),
    ("\"\\'\"  ", "\"\\'\"", "'"),
    ('"\\""  ', '"\\""', '"'),
])
def test_string_escapes(src, expected_lexeme, expected_literal):
    """Run granular tests for supported string escapes."""
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.STRING
    assert scanner.tokens[0].lexeme == expected_lexeme
    assert scanner.tokens[0].literal == expected_literal
    assert scanner.tokens[0].line == 1


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    ('"\\x41"', '"\\x41"', "A"),
    ('"\\x0a"', '"\\x0a"', "\n"),
    ('"\\x1"', '"\\x1"', "\x01"),
    ('"\\u0041"', '"\\u0041"', "A"),
    ('"\\u00e9"', '"\\u00e9"', "\u00e9"),
    ('"\\u1"', '"\\u1"', "\x01"),
    ('"\\U00000041"', '"\\U00000041"', "A"),
    ('"\\U0001F600"', '"\\U0001F600"', "\U0001f600"),
])
def test_string_unicode_hex_escapes(src, expected_lexeme, expected_literal):
    """\\x (up to 2 hex), \\u (up to 4), \\U (up to 8); variable-length hex ok."""
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.STRING
    assert scanner.tokens[0].lexeme == expected_lexeme
    assert scanner.tokens[0].literal == expected_literal
    assert scanner.tokens[0].line == 1


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    (r'"\101"', r'"\101"', "A"),           # octal 101 -> 0x41
    (r'"\12"', r'"\12"', "\n"),           # octal 12 -> 10
    (r'"\7"', r'"\7"', "\x07"),
    (r'"\0"', r'"\0"', "\x00"),
    (r'"\377"', r'"\377"', "\xff"),       # max byte in octal
    (r'"\40"', r'"\40"', " "),            # space
    (r'"\1"', r'"\1"', "\x01"),           # one octal digit
])
def test_string_octal_escapes(src, expected_lexeme, expected_literal):
    r"""\<octal>{1,3} via decode_numeric_escape (base 8, up to 3 digits)."""
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.STRING
    assert scanner.tokens[0].lexeme == expected_lexeme
    assert scanner.tokens[0].literal == expected_literal
    assert scanner.tokens[0].line == 1


@pytest.mark.parametrize("src,expected_lexeme", [
    ("x", "x"),
    ("_", "_"),
    ("abc", "abc"),
    ("abc123", "abc123"),
    ("foo-bar", "foo-bar"),
    ("foo.bar", "foo.bar"),
    ("_under_score_", "_under_score_"),
    ("list-ref", "list-ref"),
    ("true", "true"),  # not a keyword until you add keyword lexing
])
def test_identifiers_single_token(src, expected_lexeme):
    """Identifiers: greedy run until delimiter; hyphen/dot allowed by scanner."""
    token = scan_single_lexeme(src)
    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == expected_lexeme
    assert token.literal is None
    assert token.line == 1


def test_string_unicode_surrogate_pair_emoji():
    """High + low surrogate \\uD83D\\uDE00 -> U+1F600"""
    src = r'"\uD83D\uDE00"'
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.STRING
    assert scanner.tokens[0].lexeme == src
    assert scanner.tokens[0].literal == "\U0001f600"
    assert scanner.tokens[0].line == 1


@pytest.mark.parametrize(
    "src",
    [
        r'"\uD800"    ',           # high surrogate, no \u low follows
        r'"\uD83D"',          # high surrogate, end of string
        r'"\uD83D\u1234"',    # high + invalid low (not in DC00-DFFF)
        r'"\uD83D   \uDE00"',    # high + low (separated by whitespace)
        r'"\uD83D bruh"',    # high + non-hex low 
    ],
)
def test_string_surrogate_pair_errors(src):
    """Incomplete or invalid surrogate encoding reports surrogate error."""
    reporter = RecordingErrorReporter()
    scanner = Scanner(src, reporter)
    scanner.scan_tokens()
    assert any(
        "surrogate" in msg.lower()
        for _line, msg in reporter.errors
    ), f"expected surrogate-related error, got {reporter.errors!r}"


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    ("1", "1", Fraction(1)),
    ("123412345678908765432234567890", "123412345678908765432234567890",
     Fraction("123412345678908765432234567890")),
    ("-12", "-12", Fraction(-12)),
    ("+12", "+12", Fraction(+12)),
])
def test_integers(src, expected_lexeme, expected_literal):
    """Run granular tests for integer number literals."""
    token = scan_single_lexeme(src)
    assert token.type == TokenType.NUMBER
    assert token.lexeme == expected_lexeme
    assert token.literal == expected_literal
    assert token.line == 1


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    ("1.0", "1.0", Fraction("1.0")),
    ("0.1", "0.1", Fraction("0.1")),
    (".0", ".0", Fraction(".0")),
    ("0.", "0.", Fraction("0."))
])
def test_decimal_number(src, expected_lexeme, expected_literal):
    """Run granular tests for decimal numbers."""
    token = scan_single_lexeme(src)
    assert token.type == TokenType.NUMBER
    assert token.lexeme == expected_lexeme
    assert token.literal == expected_literal
    assert token.line == 1


def test_eof():
    """Test EOF behavior is correct."""
    scanner = Scanner("   ", ErrorReporter())
    scanner.scan_tokens()
    token = scanner.tokens[0]
    assert token.type == TokenType.EOF
    assert token.lexeme == ""
    assert token.literal is None
    assert token.line == 1


@pytest.mark.parametrize("src,expected_lexeme,expected_literal", [
    ("1/2", "1/2", Fraction(1, 2)),
    ("-1/2", "-1/2", Fraction(-1, 2)),
    ("+1/2", "+1/2", Fraction(1, 2)),
    ("123239438/123432488", "123239438/123432488",
     Fraction(123239438, 123432488)),
])
def test_fractions_valid(src, expected_lexeme, expected_literal):
    """Run granular tests for valid fraction literals."""
    token = scan_single_lexeme(src)
    assert token.type == TokenType.NUMBER
    assert token.lexeme == expected_lexeme
    assert token.literal == expected_literal
    assert token.line == 1


@pytest.mark.parametrize("src", [
    "-1/-2",
    "-1/+2",
    "+1/+2",
    "1/-2",
    "1/+2",
    "1//2",
    "1/",
    "/2",
])
def test_fractions_invalid(src):
    """Run granular tests for invalid fraction forms."""
    token = scan_single_lexeme(src)
    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == src
    assert token.literal is None
    assert token.line == 1


@pytest.mark.parametrize("lexeme,expected_base,expected_exponent", [
    ("1e4", Fraction("1"), 4),
    ("10e-4", Fraction("10"), -4),
    ("1.23e4", Fraction("1.23"), 4),
    ("1.23e-4", Fraction("1.23"), -4),
    ("1.23E+4", Fraction("1.23"), 4),
    ("0e0", Fraction("0"), 0),
    ("12E0", Fraction("12"), 0),
    ("001e02", Fraction("1"), 2),
    ("1.e4", Fraction("1."), 4),
    (".5e4", Fraction(".5"), 4),
    ("-1e4", Fraction("-1"), 4),
    ("+1e4", Fraction("+1"), 4),
    ("1/2e4", Fraction(1, 2), 4),
])
def test_scientific_notation_valid(lexeme, expected_base, expected_exponent):
    token = scan_single_lexeme(lexeme)
    assert token.type == TokenType.NUMBER
    assert token.lexeme == lexeme
    assert isinstance(token.literal, ScientificNotation)
    assert token.literal.base == expected_base
    assert token.literal.exponent == expected_exponent
    assert token.line == 1


@pytest.mark.parametrize(
    "lexeme",
    [
        "e10",      # missing coefficient
        "1e",       # missing exponent digits
        "1e+",      # sign but no exponent digits
        "1/2e-1/2", # invalid exponent
        "1/23e0.5", # exponent not integer
        "1E",       # uppercase exponent marker without exponent digits
        "1e-",
        "1e+",
    ],
)
def test_scientific_notation_invalid(lexeme):
    token = scan_single_lexeme(lexeme)
    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == lexeme
    assert token.literal is None
    assert token.line == 1


@pytest.mark.parametrize("lexeme,real_part,imaginary_part", [
    ("1+2i", Fraction("1"), Fraction("2")),
    ("1-2i", Fraction("1"), Fraction("-2")),
    ("1+i", Fraction("1"), Fraction("1")),
    ("1-i", Fraction("1"), Fraction("-1")),
    ("1+0i", Fraction("1"), Fraction("0")),
    ("1-0i", Fraction("1"), Fraction("0")),
    ("+2i", Fraction("0"), Fraction("2")),
    ("-2i", Fraction("0"), Fraction("-2")),
    ("0+1i", Fraction("0"), Fraction("1")),
    ("0-1i", Fraction("0"), Fraction("-1")),
    ("0+0i", Fraction("0"), Fraction("0")),
    ("0-0i", Fraction("0"), Fraction("0")),
    ("-i", Fraction("0"), Fraction("-1")),
    ("+i", Fraction("0"), Fraction("1")),
])
def test_complex_numbers_valid(lexeme, real_part, imaginary_part):
    token = scan_single_lexeme(lexeme)
    assert token.type == TokenType.NUMBER
    assert token.lexeme == lexeme
    assert isinstance(token.literal, Complex)
    assert token.literal.real_part == real_part
    assert token.literal.imaginary_part == imaginary_part
    assert token.line == 1


@pytest.mark.parametrize("lexeme", [
    "1+2",       # missing trailing i
    "1-2",       # missing trailing i
    "i",         # missing real and imaginary numeric parts
    "1++2i",     # invalid operator sequence
    "1+-2i",     # invalid operator sequence
    "1--2i",     # invalid operator sequence
    "1/2+3/4",   # missing trailing i
    "1/2+3/4ii", # extra trailing i
])
def test_complex_numbers_invalid(lexeme):
    token = scan_single_lexeme(lexeme)
    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == lexeme
    assert token.literal is None
    assert token.line == 1


@pytest.mark.parametrize("src,expected_string", [
    ("\"bruh", "unterminated"),
    ("\"bruh \\\"", "unterminated"),
])
def test_unterminated_string(src, expected_string):
    reporter = RecordingErrorReporter()
    scanner = Scanner(src, reporter)
    scanner.scan_tokens()

    assert any(
        expected_string in report.lower()
        for line, report in reporter.errors
    ), f"Expected unterminated string but got {reporter.errors!r}"


@pytest.mark.parametrize("src,expected_string", [
    ('"\\z"', "escape sequence."),
    ('"\\p"', "escape sequence."),
    ('"\\;"', "escape sequence.")
])
def test_invalid_escape(src, expected_string):
    reporter = RecordingErrorReporter()
    scanner = Scanner(src, reporter)
    scanner.scan_tokens()

    assert any(
        expected_string in error
        for line, error in reporter.errors
    ), f"Expected Invalid escape sequence but got: {reporter.errors!r}"


@pytest.mark.parametrize("src,expected_string", [
    ("#tru", " '#'"),
    ("#fal", " '#'"),
    ("##bruh", " '#'")
])
def test_invalid_booleans_(src, expected_string):
    reporter = RecordingErrorReporter()
    scanner = Scanner(src, reporter)
    scanner.scan_tokens()

    assert any(
        expected_string in error
        for line, error in reporter.errors
    ), f"Expected invalid escape sequence but got: {reporter.errors!r}"


def test_scan_integration_mixed_tokens():
    """One line mixing parens, complex, id, octal string, bool, scientific, brackets."""
    src = r'(+1-2i foo.bar "\101" #false 3.14e-2 [a,b])'
    scanner = Scanner(src, ErrorReporter())
    scanner.scan_tokens()
    toks = scanner.tokens
    assert toks[-1].type == TokenType.EOF
    assert len(toks) == 13

    assert toks[0].type == TokenType.LEFT_PAREN and toks[0].lexeme == "("

    assert toks[1].type == TokenType.NUMBER and toks[1].lexeme == "+1-2i"
    assert isinstance(toks[1].literal, Complex)
    assert toks[1].literal.real_part == Fraction(1)
    assert toks[1].literal.imaginary_part == Fraction(-2)

    assert toks[2].type == TokenType.IDENTIFIER and toks[2].lexeme == "foo.bar"

    assert toks[3].type == TokenType.STRING and toks[3].lexeme == r'"\101"'
    assert toks[3].literal == "A"

    assert toks[4].type == TokenType.BOOLEAN and toks[4].lexeme == "#false"
    assert toks[4].literal is False

    assert toks[5].type == TokenType.NUMBER and toks[5].lexeme == "3.14e-2"
    assert isinstance(toks[5].literal, ScientificNotation)
    assert toks[5].literal.base == Fraction("3.14")
    assert toks[5].literal.exponent == -2

    assert toks[6].type == TokenType.LEFT_BRACK and toks[6].lexeme == "["
    assert toks[7].type == TokenType.IDENTIFIER and toks[7].lexeme == "a"
    assert toks[8].type == TokenType.COMMA and toks[8].lexeme == ","
    assert toks[9].type == TokenType.IDENTIFIER and toks[9].lexeme == "b"
    assert toks[10].type == TokenType.RIGHT_BRACK and toks[10].lexeme == "]"
    assert toks[11].type == TokenType.RIGHT_PAREN and toks[11].lexeme == ")"

    for t in toks[:-1]:
        assert t.line == 1
