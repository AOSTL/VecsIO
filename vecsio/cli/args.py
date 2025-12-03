import sys
import argparse
from .commands import *

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vecsio")
    subparsers = parser.add_subparsers(dest="command")

    metadata_parser = subparsers.add_parser(
        METADATA[0],
        help="Show metadata for vec files",
        aliases=METADATA[1:],
        usage="vecsio metadata <path_to_vecs_file>"
    )
    metadata_parser.add_argument("path", help="Path to .fvecs or .ivecs file", type=str)

    inspect_parser = subparsers.add_parser(
        INSPECT[0],
        help="Inspect vec files",
        aliases=INSPECT[1:],
        usage="vecsio inspect <path_to_vecs_file>"
    )
    inspect_parser.add_argument("path", help="Path to .fvecs or .ivecs file", type=str)
    inspect_parser.add_argument(
        "-s",
        "--start",
        nargs = "*",
        metavar = ("ROW", "COL"),
        type = int,
        default = [0, 0],
        help = "Start coordinate; ROW default=0, COL default=0"
    )
    inspect_parser.add_argument(
        "-e",
        "--end",
        nargs = "*",
        metavar = ("ROW", "COL"),
        type = int,
        default = [],
        help = "End coordinate; ROW default=<Input_Row>, COL default=-1"
    )
    inspect_parser.add_argument(
        "-t",
        "--transpose",
        action="store_true",
        help="Transpose the selected block before printing"
    )
    inspect_parser.add_argument(
        "--show-axis",
        action="store_true",
        help="Show coordinate axes when printing"
    )
    inspect_parser.add_argument(
        "--axis-origin",
        choices=("selection", "zero"),
        default="selection",
        help="Axis labels start from the selection start or from 0"
    )

    return parser

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    return args