#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict
from .bsl_token import BslToken
from .error_reporter import ErrorReporter


class Environment():
    values: Dict[str, object] = field({})

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: BslToken):
        if name.lexeme in self.values:
            return self.values[name.lexeme]




if __name__ == "__main__":
    print("Hello World.")
