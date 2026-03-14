#!/usr/bin/env python3
from token_type import TokenType


class BslToken:
    """Implements Token Class."""

    def __init__(self,
                 type: TokenType,
                 lexeme: str,
                 literal: object,
                 line: int):
        """Initialize the values of the token."""
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        """Get the human-readable string representation of the token."""
        return f"{self.type} {self.lexeme} {self.literal}"


# test_token = Token(TokenType.LEFT_PAREN, "(", None, 12)

# test_token.to_string()
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#     def greet(self):
#         print(f"Hello, my name is {self.name} and age {self.age}")

# john = Person("John", 36)
# john.greet()
