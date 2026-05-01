#!/usr/bin/env python3
from .ast import Expr, ProcedureCall, Literal, Variable, DefineVar
from .scanner import Scanner
from .parser import Parser
from .error_reporter import ErrorReporter
from .ast_printer import print_ast
from .token_type import TokenType
from fractions import Fraction
from .numbers import Complex
from .runtime_error import BslRuntimeError
from .environment import Environment

def interpret(expressions: [Expr]):
    """Interpreter multiple expressions in a program."""

    environment = Environment()

    try:
        for expression in expressions:
            print(evaluate(expression, environment))
    except BslRuntimeError:
        raise BslRuntimeError()


def evaluate(expression: Expr, environment: Environment):
    """Interpret/evaluate a given expression."""
    match expression:
        case Literal(value=value):
            return value
        case Variable(name=name):
            return environment.get(name.lexeme)
        case DefineVar():
            return define(expression, environment)
        # case DefineProc(name=name, value=value):
        #     return
        case ProcedureCall(callee=callee, args=args, token=_):
            if callee.name.lexeme == "+":
                return add(args, environment)
            elif callee.name.lexeme == "-":
                return minus(args, environment)
            elif callee.name.lexeme == "*":
                return multiplication(args, environment)


# TODO: Implement all the BSL special forms
def define(definition: DefineVar, environment: Environment):
    """Define a new variable in scope and """
    value = None
    if definition.initializer is not None:
        value = evaluate(definition.initializer, environment)

    environment.define(definition.name.lexeme, value)
    return value


# TODO: Implement the following as proper BSL functions 
def add(args: [Expr], environment: Environment) -> Literal:
    """Add a list of numbers together."""
    accumulator = 0
    for arg in args:
        accumulator += evaluate(arg, environment)
    return accumulator


def minus(args: [Expr], environment: Environment) -> Literal:
    """Subtracts a list of numbers by each other."""
    if len(args) == 1:
        return -evaluate(args[0], environment)

    # first arg is minused from every argument after thus we initialize the
    # accumulator with the first arg then pop it
    accumulator = args[0].value
    args.pop(0)

    for arg in args:
        accumulator -= evaluate(arg, environment)
    return accumulator


def multiplication(args: [Expr], environment: Environment) -> object:
    """Multiplies a list of number together."""
    accumulator = 1
    for arg in args:
        accumulator *= evaluate(arg, environment)
    return accumulator


def run_program():
    scanner = Scanner("""(define x 1) (+ x x) x""", ErrorReporter())
    # scanner = Scanner("""(+ 1 1 (- 1 1) (* 2 2 2)) (+ 1 1)""",
    # ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens
    print("tokens: ", tokens)

    if tokens is None:
        print("scanning failed")
        return

    parser = Parser(tokens, ErrorReporter())
    expressions = parser.parse()
    # print("parsed: ", expressions)

    if expressions is None:
        print("parsing failed")
        return

    for expression in expressions:
        print(expression)

    interpret(expressions)


if __name__ == "__main__":
    run_program()
