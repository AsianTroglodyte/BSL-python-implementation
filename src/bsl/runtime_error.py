#!/usr/bin/env python3
from .bsl_token import BslToken


class BslRuntimeError(Exception):
    def __init__(self, token: BslToken, message: str):
        super().__init__(message)
        self.token = token
