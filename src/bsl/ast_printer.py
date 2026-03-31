from .ast import Expr, ProcedureCall, Literal, Variable
from .scanner import Scanner
from .parser import Parser
from .error_reporter import ErrorReporter


def print_ast(expression: Expr):
    """Print AST."""

    match expression:
        case Literal(value=value):
            return str(value)
        case Variable(name=name):
            return name.lexeme
        case ProcedureCall(callee=callee, args=args, token=_):
            if len(args) != 0:
                args_text = " ".join(print_ast(arg) for arg in args)
                return f"({print_ast(callee)} {args_text})"
            return f"({print_ast(callee)})"


if __name__ == "__main__":
    # scanner = Scanner("""(+ 1 2 (+ 1 2))""", ErrorReporter())
    scanner = Scanner("""(+ 1 2""", ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens

    parser = Parser(tokens, ErrorReporter())
    ast = parser.parse()

    print(print_ast(ast))

    for token in tokens:
        print(token)
