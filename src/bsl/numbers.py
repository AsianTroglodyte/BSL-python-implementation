import re
from fractions import Fraction
from .regular_expressions import EXACT_REAL, FRACTION
# Complex object for literal, internal representation of value.
class Complex:

    def __init__(self, text: str):
        complex_number = re.fullmatch(
            rf"([+-]?{EXACT_REAL})([+-]{EXACT_REAL})i",
            text
        )
        real_part, imaginary_part = complex_number.groups()

        self.real_part = Fraction(real_part)
        self.imaginary_part = Fraction(imaginary_part)
        # print(self.rea 

    def to_string(self) -> str:
        """Get the human-readable string representation of complex number."""
        return f"{self.real_part}+{self.imaginary_part}i"

    def __str__(self):
        return f"{self.real_part}+{self.imaginary_part}i"

    def __repr__(self):
        return f"{self.real_part}+{self.imaginary_part}i"


class ScientificNotation:

    def __init__(self, text: str):
        scientific_notation = re.fullmatch(
            rf"([+-]?(?:{EXACT_REAL}|{FRACTION}))[eE]([+-]?\d+)",
            text
        )
        self.base = Fraction(scientific_notation.group(1))
        self.exponent = int(scientific_notation.group(2))

    def to_string(self) -> str:
        """Get the human-readable string representation of scientific notation."""
        return f"{self.base}e{self.exponent}"

    def __str__(self):
        return f"{self.base}e{self.exponent}"

    def __repr__(self):
        return f"{self.base}e{self.exponent}"