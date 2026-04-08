#!/usr/bin/env python3
from dataclasses import dataclass
from .bsl_token import BslToken

class Expr:
    """Shared class to add more type information and errors."""

    pass


# strings, numbers, booleans, and Identifiers
@dataclass
class Literal(Expr):
    """Stores literal values."""

    value: object


@dataclass
class Variable(Expr):
    """Stores variable name."""

    name: BslToken


# function calls: pretty much all procedures in BSL
@dataclass
class ProcedureCall(Expr):
    """
    Represent any procedure call such as '+' or some other user-defined
    procedure.
    """

    callee: Variable
    args: tuple[Expr]
    token: BslToken


@dataclass
class SpecialForm(Expr):
    """Define a node type: the special form."""

    pass


@dataclass
class DefineVar(SpecialForm):
    """Create the Define AST node."""

    name: BslToken
    value: Expr


class DefineProc(SpecialForm):
    """Create the AST node for defining a procedure."""

    name: BslToken
    value: Expr


@dataclass
class Cond(SpecialForm):
    """Created the Cond AST node."""

    args: tuple[Expr]


@dataclass
class Logical(SpecialForm):
    """Create the And AST node special form."""

    args: tuple[Expr]
