#!/usr/bin/env python3
import sys

from .bsl import Bsl


def main() -> None:
    """Run the BSL interpreter entrypoint."""
    args = sys.argv[1:]
    Bsl().entry_point(args)


if __name__ == "__main__":
    main()
