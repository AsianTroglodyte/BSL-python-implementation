#!/usr/bin/env python3
from bsl.token_type import TokenType
from bsl.error_reporter import ErrorReporter
from bsl.scanner import Scanner
from bsl.bsl_token import BslToken


def test_scanner():
    scanner = Scanner("() ) {} } \n [] ]", ErrorReporter())
    scanner.scan_tokens()

    # Uses decorator to allow for equality.
    assert scanner.tokens == [BslToken(TokenType.LEFT_PAREN, '(', None, 1),
                              BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
                              BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
                              BslToken(TokenType.LEFT_BRACE, '{', None, 1),
                              BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
                              BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
                              BslToken(TokenType.LEFT_BRACK, '[', None, 2),
                              BslToken(TokenType.RIGHT_BRACK, ']', None, 2),
                              BslToken(TokenType.RIGHT_BRACK, ']', None, 2),
                              BslToken(TokenType.EOF, "", None, 2)]

# class TestScanner(unittest.TestCase):
#     """"Run tests on the scanner class"""

#     def test_all_parens(self):
#         """Test if all possible parentheses are permitted."""
#         scanner = Scanner("() ) {} } \n [] ]", error_reporter)
#         scanner.scan_tokens()

#         # Uses decorator to allow for equality.
#         assert scanner.tokens == [BslToken(TokenType.LEFT_PAREN, '(', None, 1),
#                                   BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
#                                   BslToken(TokenType.RIGHT_PAREN, ')', None, 1),
#                                   BslToken(TokenType.LEFT_BRACE, '{', None, 1),
#                                   BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
#                                   BslToken(TokenType.RIGHT_BRACE, '}', None, 1),
#                                   BslToken(TokenType.RIGHT_BRACK, '[', None, 2),
#                                   BslToken(TokenType.LEFT_BRACK, ']', None, 2),
#                                   BslToken(TokenType.LEFT_PAREN, ']', None, 2),
#                                   BslToken(TokenType.EOF, "", None, 2)]

# if __name__ == '__main__':
#     print("start")
#     from .error_reporter import ErrorReporter

#     error_reporter = ErrorReporter()
#     scanner = Scanner("(){}[],#;`\"bruh\"\n123 bruh", error_reporter)
#     scanner.scan_tokens()

#     for token in scanner.tokens:
#         print(f"token: {token.to_string()}")
#     print("end")

    # def test_string(self):
    #     scanner = Scanner("""\"bruh\"
    #                       \"1234567890-=!@#$%^&*()_+qwertyuiop
    #                       []asdfghjkl;'zxcvbnm,./{}|:<>?\"
    #                       """"",
    #                       error_reporter)

    #     scanner.scan_tokens()
    # def test_number(self):


# if  __name__ == '__main__':
#     unittest.main()
