#!/usr/bin/env python3
from .token_type import TokenType
from dataclasses import dataclass


@dataclass
class BslToken:
    """Implements Token Class."""

    def __init__(self,
                 type: TokenType,
                 lexeme: str,
                 literal: object,
                 line: int):
        """Initialize the values of the token."""
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        """Get the human-readable string representation of the token."""
        return f"{self.type} {self.lexeme} {self.literal}"
