#!/usr/bin/env python3
from .bsl_token import BslToken
from typing import List
from .scanner import Scanner
from .error_reporter import ErrorReporter
from .token_type import TokenType
from .ast import ProcedureCall, Literal, Variable


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
        try:
            return self.expression()
        except parser.ParseError:
            self.synchronize()
            return None

    def expression(self):
        """Everything in BSL is an expression."""
        if self.match([TokenType.LEFT_PAREN]):
            return self.procedure_call()
        elif self.peek().type in [
                TokenType.IDENTIFIER,
                TokenType.STRING,
                TokenType.NUMBER,
                TokenType.TRUE,
                TokenType.FALSE]:
            return self.primary()
        else:
            self.error_reporter.error_token(self.peek(), "Expect expression.")

    def procedure_call(self):
        """Parse a possible procedure call."""
        # self.advance()

        args: List[BslToken] = []

        callee = self.primary()

        # first check if the call has no arguments by checking if current
        # TokenType has no RIGHT_PAREN
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self.expression())
                # print("args: ", args)
                if self.peek().type == TokenType.RIGHT_PAREN:
                    break
                elif self.peek().type == TokenType.EOF:
                    break

        # we use paren to record error reporting information.
        # We also use consume as it will throw an error if the next TokenType
        # is NOT RIGHT_PAREN
        # print("final args: ", args)
        paren = self.consume(
            TokenType.RIGHT_PAREN,
            "Expect ')' after arguments.")

        return ProcedureCall(callee, args, paren)

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
        """
        Check if current token has any of the given type.
        If so it consumes the token and returns true.
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
        raise self.error_reporter.error_token(self.peek(), message)

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
            self.error_reporter.report(token.line, f" at '{token.lexeme}'", message)
        return self.ParseError()


if __name__ == '__main__':
    from pprint import pprint
    from dataclasses import asdict
    """(IDENTIFIER )"""

    # scanner = Scanner("""(+ (+ 1 2(+ 1 2 3)) (- 1 1 2 3 4))""", ErrorReporter())
    scanner = Scanner("""if (+ 1 2)""", ErrorReporter())
    scanner.scan_tokens()
    tokens = scanner.tokens

    parser = Parser(tokens, ErrorReporter())
    ast = parser.parse()

    if ast is not None:
        print(ast)

        pprint(asdict(ast), width=100, sort_dicts=False)

        for token in tokens:
            print(token)

# def run_quick_test():
