#!/usr/bin/env python3
from .ast import Expr, ProcedureCall, Literal, Variable
from .scanner import Scanner
from .parser import Parser
from .error_reporter import ErrorReporter
from .ast_printer import print_ast
from .token_type import TokenType
from fractions import Fraction
from .numbers import Complex

def interpret(expression: Expr):
    """Interpret/evaluate a given expression."""

    match expression:
        case Literal(value=value):
            return value
        case Variable(name=name):
            return name.lexeme
        case ProcedureCall(callee=callee, args=args, token=_):
            if callee.name.lexeme == "+":
                return add(args)
            if callee.name.lexeme == "-":
                return minus(args)
            if callee.name.lexeme == "*":
                return multiplication(args)


# TODO: Implement the following as proper BSL functions 
def add(args: [Expr]) -> Literal:
    """Add a list of numbers together."""
    accumulator = 0
    for arg in args:
        accumulator += interpret(arg)
    return accumulator


def minus(args: [Expr]) -> Literal:
    """Subtracts a list of numbers by each other."""
    if len(args) == 1:
        return -interpret(args[0])

    # first arg is minused from every argument after thus we initialize the
    # accumulator with the first arg then pop it
    accumulator = args[0].value
    args.pop(0)

    for arg in args:
        accumulator -= interpret(arg)
    return accumulator


def multiplication(args: [Expr]) -> object:
    """Multiplies a list of number together."""
    accumulator = 1
    for arg in args:
        accumulator *= interpret(arg)
    return accumulator


if __name__ == "__main__":
    # scanner = Scanner("""(+ 1 2 (+ 1 2))""", ErrorReporter())
    scanner = Scanner("""(+ 1 1 (- 1 1) (* 2 2 2))""", ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens

    parser = Parser(tokens, ErrorReporter())
    ast = parser.parse()

    print(print_ast(ast))

    print(interpret(ast))

    # for token in tokens:
    #     print(token)
