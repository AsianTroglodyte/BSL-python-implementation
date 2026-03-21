import re
from fractions import Fraction
from .regular_expressions import EXACT_REAL, FRACTION
# Complex object for literal, internal representation of value.


class Complex:
    real_part: Fraction
    imaginary_part: Fraction

    def __init__(self, text: str):
        complex_number = re.fullmatch(
            rf"([+-]?{EXACT_REAL})?([+-](?:{EXACT_REAL})?)i",
            text
        )
        real_part, imaginary_part = complex_number.groups()

        if real_part is None:
            real_part = 0

        # probably a cleaner way to do this but oh well if there was not
        # coefficent for the imaginary_part we get either "+" or "-" in the
        # case of +i or -i how we handle it is below scrappy but it works
        if imaginary_part == "+":
            imaginary_part = 1
        elif imaginary_part == "-":
            imaginary_part = -1

        print(f"complex_number: {complex_number}")

        print(f"real_part: {real_part}\nimaginary_part: {imaginary_part}")

        self.real_part = Fraction(real_part)
        self.imaginary_part = Fraction(imaginary_part)

    def to_string(self) -> str:
        """Get the human-readable string representation of complex number."""
        return f"{self.real_part}+{self.imaginary_part}i"

    def __str__(self):
        return f"{self.real_part}+{self.imaginary_part}i"

    def __repr__(self):
        return f"{self.real_part}+{self.imaginary_part}i"


class ScientificNotation:
    base: Fraction
    exponent: int

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
