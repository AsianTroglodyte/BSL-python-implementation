#!/usr/bin/env python3
from .bsl_token import BslToken
from typing import List
from .scanner import Scanner
from .error_reporter import ErrorReporter
from .token_type import TokenType
from .ast import ProcedureCall, Literal, Variable, DefineVar, DefineProc, Logical, Cond


class Parser:
    """
    Parses through the token list created by the scanner and constructs an AST.
    """

    tokens: List[BslToken]
    current: int = 0
    error_reporter: ErrorReporter

    class ParseError(RuntimeError):
        """Sentinel exception used to unwind parser during panic mode."""

        pass

    def __init__(
        self,
        tokens: List[BslToken] | None = None,
        error_reporter: ErrorReporter | None = None
    ):
        """Initialize parser state and optional dependencies."""
        self.tokens = tokens or []
        self.current = 0
        self.error_reporter = error_reporter or ErrorReporter()

    def init(self, tokens: List[BslToken]):
        """Initialize the Parser with the List of BSL Tokens."""
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """Parse one top-level expression with panic-mode recovery."""
        expressions = []

        while not self.isAtEnd():
            try:
                expressions.append(self.expression())
                # print(f"expression: {expressions}")
            except self.ParseError:
                self.synchronize()
                return None

        return expressions

    def expression(self):
        """Everything in BSL is an expression."""
        if self.match([TokenType.LEFT_PAREN]):
            # The following handle special forms. They have special structures
            # and have special evaluations rules.
            # Do NOT use match() because procedure call must call primary()
            # to consume and store the
            if self.match([TokenType.COND]):
                return self.cond()
            elif self.match([TokenType.DEFINE]):
                return self.define()
            elif self.match([TokenType.AND]) or self.match([TokenType.OR]):
                return self.logical()
            # regular user-defined or built in functions are handled by
            # this code path
            elif self.match([TokenType.IDENTIFIER]):
                return self.procedure_call()
            # a LEFT_PAREN is always followed up
            # with some IDENTIFIER or "keyword"
            else:
                self.error(self.peek(), "function call: expected a function" \
                           "after the open parenthesis, but found a part")
        elif self.peek().type in [
                TokenType.IDENTIFIER,
                TokenType.STRING,
                TokenType.NUMBER,
                TokenType.TRUE,
                TokenType.FALSE]:
            return self.primary()
        else:
            self.error(self.peek(), "Expect expression.")

    def procedure_call(self):
        """Parse a possible procedure call."""
        args: List[BslToken] = []

        callee = self.primary()
        if not isinstance(callee, Variable):
            self.error(self.previous(), "Expect Variable")

        # first check if the call has no arguments by checking if current
        # TokenType has no RIGHT_PAREN
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self.expression())
                if self.peek().type == TokenType.RIGHT_PAREN:
                    break
                elif self.peek().type == TokenType.EOF:
                    break

        # we use paren to record error reporting information.
        # We also use consume as it will throw an error if the next TokenType
        # is NOT RIGHT_PAREN
        paren = self.consume(
            TokenType.RIGHT_PAREN,
            "Expect ')' after arguments.")

        return ProcedureCall(callee, args, paren)

    def define(self):
        """Parse through a define expression/special form."""

        name = self.consume(
            TokenType.IDENTIFIER, "define: expected a" \
            "variable name, or a function name and its variables (in" \
            f"parentheses), but found a {self.peek().type}")

        value = self.expression()

        self.consume(TokenType.RIGHT_PAREN,
                     "read-syntax: expected a `)` to close `(`")

        return DefineVar(name, value)

    def cond(self):
        """Evaluate Cond expressions, special forms."""
        args = ()

        return Cond(args)

    # named as such because "and" is a reserved word
    def logical(self):
        """Evaluate "and" expressions, special forms."""
        args = [BslToken]

        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self.expression())
                # print("args: ", args)
                if self.peek().type == TokenType.RIGHT_PAREN:
                    break
                elif self.peek().type == TokenType.EOF:
                    break
        return Logical(args)

    def primary(self):
        """Parse literals, expressions, and identifiers."""
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)

        if self.match([TokenType.IDENTIFIER]):
            return Variable(self.previous())

    def match(self, types: List[TokenType]) -> bool:
        """Check if current token has any of the given type. If so it consumes
        the token and returns true.
        """
        for token_type in types:
            if (self.check(token_type)):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> BslToken:
        """Consume expected token or raise parse error."""
        if (self.check(token_type)):
            return self.advance()
        raise self.error(self.peek(), message)

    def synchronize(self) -> None:
        """Enter panic mode and advance to likely statement boundary."""
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (TokenType.IF, TokenType.COND):
                return

            self.advance()

    def check(self, token_type: TokenType) -> bool:
        """Return true if the current token is of the given type."""
        if (self.isAtEnd()):
            return False

        return self.peek().type == token_type

    def advance(self) -> BslToken:
        """Consumes current token sand returns it."""
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    def isAtEnd(self) -> bool:
        """Check if we've run out of tokens to partse."""
        return self.peek().type == TokenType.EOF

    def peek(self) -> BslToken:
        """Return the current token we have yet to consume."""
        return self.tokens[self.current]

    def previous(self) -> BslToken:
        """Return the most recently consumed token."""
        return self.tokens[self.current - 1]

    def error(self, token: BslToken, message: str) -> ParseError:
        """Report parse error at token and return ParseError sentinel."""
        if token.type == TokenType.EOF:
            self.error_reporter.report(token.line, " at end", message)
        else:
            self.error_reporter.report(
                token.line,
                f" at '{token.lexeme}'",
                message)
        return self.ParseError()


if __name__ == '__main__':
    from pprint import pprint
    from dataclasses import asdict
    """(IDENTIFIER )"""

    # scanner = Scanner("""(+ (+ 1 2(+ 1 2 3)) (- 1 1 2 3 4))""", ErrorReporter())
    scanner = Scanner("""(define abc 1 )""", ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens
    for token in tokens:
        print(token)

    parser = Parser(tokens, ErrorReporter())
    ast = parser.parse()
    print(ast)

    if ast is not None:

        pprint(asdict(ast), width=100, sort_dicts=False)

        for token in tokens:
            print(token)

# def run_quick_test():
