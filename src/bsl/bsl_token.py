#!/usr/bin/env python3
from .token_type import TokenType
from dataclasses import dataclass


@dataclass
class BslToken:
    """Implements Token Class."""

    type: TokenType
    lexeme: str
    literal: object
    line: int

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
