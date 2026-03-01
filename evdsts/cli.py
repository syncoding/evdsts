"""evdsts command-line interface"""

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="evdsts",
        description="evdsts - TCMB EVDS time series toolkit",
    )
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser(
        "build-index",
        help="Build or rebuild the EVDS series search index.",
    )
    build_parser.add_argument(
        "--language",
        choices=["TR", "ENG"],
        default="TR",
        help="Index language (default: TR)",
    )
    build_parser.add_argument(
        "--wait",
        type=float,
        default=5,
        help="Seconds to wait between API requests (default: 5, min: 5)",
    )
    build_parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="EVDS API key (reads from saved key file if not provided)",
    )
    build_parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "build-index":
        from evdsts.base.indexing import IndexBuilder

        builder = IndexBuilder(key=args.key, language=args.language)
        builder.build_index(wait=args.wait, confirm=not args.yes)


if __name__ == "__main__":
    main()
