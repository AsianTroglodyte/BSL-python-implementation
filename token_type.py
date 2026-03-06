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
    POUND = 8
    SEMICOLON = 9
    BACK_TICK = 10

    # Literals.
    IDENTIFIER = 9
    STRING = 10
    NUMBER = 11

    # Keywords.
    IF = 12
    COND = 13

    EOF = 14
