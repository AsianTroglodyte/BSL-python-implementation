#!/usr/bin/env python3
from dataclasses import dataclass
from .bsl_token import BslToken

class Expr:
    """Shared class to add more type information and errors."""

    pass


# function calls: pretty much all procedures in BSL
@dataclass
class ProcedureCall(Expr):
    """
    Represent any procedure call such as '+' or some other user-defined
    procedure.
    """
    callee: Expr
    args: tuple[Expr]
    token: BslToken


# strings, numbers, booleans, and Identifiers
@dataclass
class Literal(Expr):
    """Stores literal values."""

    value: object


@dataclass
class Variable(Expr):
    """Stores variable name."""

    name: BslToken
