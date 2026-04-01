from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

from .regular_expressions import COMPLEX_LITERAL_RE, EXACT_REAL, FRACTION


def parse_number_token(text: str) -> Fraction | Complex:
    """
    Parse a NUMBER token lexeme to a literal value.
    Complex-shaped text with zero imaginary part becomes a plain Fraction.
    """
    m = re.fullmatch(COMPLEX_LITERAL_RE, text)
    if m is not None:
        real_part, imaginary_part = m.groups()
        if real_part is None:
            real_part = 0
        if imaginary_part == "+":
            imaginary_part = 1
        elif imaginary_part == "-":
            imaginary_part = -1
        real_f = Fraction(real_part)
        imag_f = Fraction(imaginary_part)
        if imag_f == 0:
            return real_f
        return Complex.from_parts(real_f, imag_f)

    m = re.fullmatch(
        rf"([+-]?(?:{EXACT_REAL}|{FRACTION}))[eE]([+-]?\d+)",
        text,
    )
    if m is not None:
        return Fraction(m.group(1)) * (Fraction(10) ** int(m.group(2)))
    return Fraction(text)


@dataclass(init=False)
class Complex:
    """Exact complex literal: real and imaginary parts as Fraction."""

    real_part: Fraction
    imaginary_part: Fraction

    @classmethod
    def from_parts(cls, real_part: Fraction, imaginary_part: Fraction) -> Complex:
        """Build without re-parsing source text."""
        obj = cls.__new__(cls)
        obj.real_part = real_part
        obj.imaginary_part = imaginary_part
        return obj

    def __init__(self, text: str) -> None:
        """Instantiate a complex number from source text."""
        m = re.fullmatch(COMPLEX_LITERAL_RE, text)
        if m is None:
            raise ValueError(f"invalid complex literal: {text!r}")
        real_part, imaginary_part = m.groups()
        if real_part is None:
            real_part = 0
        if imaginary_part == "+":
            imaginary_part = 1
        elif imaginary_part == "-":
            imaginary_part = -1
        self.real_part = Fraction(real_part)
        self.imaginary_part = Fraction(imaginary_part)

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Complex.from_parts(self.real_part + other,
                                      self.imaginary_part)
        elif isinstance(other, Complex):
            return Complex.from_parts(
                self.real_part + other.real_part,
                self.imaginary_part + self.imaginary_part)

    def __radd__(self, other):
        if isinstance(other, (Fraction, int)):
            return Complex.from_parts(self.real_part + other,
                                      self.imaginary_part)
