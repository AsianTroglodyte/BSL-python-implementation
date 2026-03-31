#!/usr/bin/env python3
from enum import Enum


class TokenType(Enum):
    """Enum that for all tokens."""

    # Single-character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_BRACK = 5
    RIGHT_BRACK = 6
    COMMA = 7
    SEMICOLON = 8
    BACK_TICK = 9

    # Literals.
    IDENTIFIER = 10
    STRING = 11
    NUMBER = 12

    # Keywords.
    TRUE = 13
    FALSE = 14
    IF = 15
    COND = 16

    EOF = 17
