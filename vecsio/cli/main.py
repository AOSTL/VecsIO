from __future__ import annotations

import sys
from .args import parse_args
from .actions import COMMAND_ACTIONS

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return COMMAND_ACTIONS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
