from .base import decorator_wrapper
from pathlib import Path
from typing import Any
import argparse
import sys

def _check_path_exists(args: argparse.Namespace, *_: Any, **__: Any) -> bool:
    path: Path = args.path
    if not path.exists():
        print(f"No such file or permission denied: {path}", file=sys.stderr)
        return True
    return False

path_exists = decorator_wrapper(_check_path_exists)