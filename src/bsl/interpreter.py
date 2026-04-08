#!/usr/bin/env python3
from .ast import Expr, ProcedureCall, Literal, Variable
from .scanner import Scanner
from .parser import Parser
from .error_reporter import ErrorReporter
from .ast_printer import print_ast
from .token_type import TokenType
from fractions import Fraction
from .numbers import Complex
from .runtime_error import BslRuntimeError


def interpret(expressions: [Expr]):
    """Interpreter multiple expressions in a program."""
    try:
        for expression in expressions:
            print(f"execute(expression){execute(expression)}")
    except BslRuntimeError:
        raise BslRuntimeError()


def execute(expression: Expr):
    """Interpret/evaluate a given expression."""

    match expression:
        case Literal(value=value):
            return value
        case Variable(name=name):
            return name.lexeme
        # case DefineVar(name=name, value=value):
        #     return name.lexeme
        # case DefineProc(name=name, value=value):
        #     return
        case ProcedureCall(callee=callee, args=args, token=_):
            if callee.name.lexeme == "+":
                return add(args)
            elif callee.name.lexeme == "-":
                return minus(args)
            elif callee.name.lexeme == "*":
                return multiplication(args)


# TODO: Implement all the BSL special forms


# TODO: Implement the following as proper BSL functions 
def add(args: [Expr]) -> Literal:
    """Add a list of numbers together."""
    accumulator = 0
    for arg in args:
        accumulator += execute(arg)
    return accumulator


def minus(args: [Expr]) -> Literal:
    """Subtracts a list of numbers by each other."""
    if len(args) == 1:
        return -execute(args[0])

    # first arg is minused from every argument after thus we initialize the
    # accumulator with the first arg then pop it
    accumulator = args[0].value
    args.pop(0)

    for arg in args:
        accumulator -= execute(arg)
    return accumulator


def multiplication(args: [Expr]) -> object:
    """Multiplies a list of number together."""
    accumulator = 1
    for arg in args:
        accumulator *= execute(arg)
    return accumulator


if __name__ == "__main__":
    scanner = Scanner("""(define x 1)""", ErrorReporter())
    # scanner = Scanner("""(+ 1 1 (- 1 1) (* 2 2 2)) (+ 1 1)""",
    # ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens
    print(tokens)

    parser = Parser(tokens, ErrorReporter())
    expressions = parser.parse()
    print(expressions)

    for expression in expressions:
        print(print_ast(expression))

    interpret(expressions)

    # for token in tokens:
    #     print(token)
