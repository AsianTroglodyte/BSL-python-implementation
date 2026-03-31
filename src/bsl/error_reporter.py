#!/usr/bin/env python3
from .bsl_token import BslToken
from .token_type import TokenType


class ErrorReporter:
    """Create error object to track and report errors."""
    had_error = False

    def error_line(self, line: int, message: str):
        """Throw error given a line and a particular message."""
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        """Report given a line and message."""
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True

    def error_token(self, token: BslToken, message: str):
        """Report parse error at token and return ParseError sentinel."""
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)
