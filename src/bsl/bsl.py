#!/usr/bin/env python3
from typing import List
import sys
from .scanner import Scanner
from .error_reporter import ErrorReporter


class Bsl:
    """Define Bsl class for language."""
    error_reporter = ErrorReporter()

    def entry_point(self, args: List[str]):
        """Entry point of program."""
        list_len = len(args)

        if list_len == 1:
            self.run_file(args[0])
        elif list_len == 0:
            self.run_repl()
        else:
            print("Error: invalid number of arguments")

    def run_file(self, file_name: str):
        """Run BSL program in a file from specified file path."""
        try:
            with open(file_name, "r") as f:
                content = f.read()
                scanner = Scanner(content, self.error_reporter)
                scanner.scan_tokens()
        except FileNotFoundError:
            print(f"file \"{file_name}\" was not found")

    def run_repl(self):
        """Start up a REPL."""
        while True:
            user_input = input("> ")

            if (user_input == ""):
                break

            scanner = Scanner(user_input, self.error_reporter)
            scanner.scan_tokens()


if __name__ == '__main__':
    """Start Program."""
    args = sys.argv[1:]
    startBsl = Bsl()
    startBsl.entry_point(args)
