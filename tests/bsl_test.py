#!/usr/bin/env python3
from bsl import Bsl
import unittest

class TestBsl(unittest.TestCase):
    """Run Test for the Bsl class."""

    def test_run_file(self):
        bsl = Bsl()
        bsl.run_file("example.rkt")

    def test_run_repl(self):
        self.assert
