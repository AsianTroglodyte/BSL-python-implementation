#!/usr/bin/env python3


class ErrorReporter:
    """Create error object to track and report errors."""
    had_error = False

    def error(self, line: int, message: str):
        """Throw error given a line and a particular message."""
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        """Report given a line and message."""
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True
