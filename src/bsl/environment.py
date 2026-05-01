#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, Optional
from .bsl_token import BslToken


@dataclass
class Environment:
    values: Dict[str, object] = field(default_factory=dict)
    enclosing: Optional["Environment"] = None

    def define(self, name: str, value: object) -> None:
        """Define a variable in the environment."""
        # name.lexeme is the variable name string
        self.values[name] = value

    def get(self, name: str) -> object:
        """Get a variable in the environment."""
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        # Crafting Interpreters throws a runtime error here:
        raise RuntimeError(f"Undefined variable '{name}'.")


if __name__ == "__main__":
    print("Hello World.")
