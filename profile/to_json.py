"""
Convert a Songs of Syx datagram to JSON.

Example:
    cat AppData/Roaming/songsofsyx/saves/profile/SavedPrints.txt \
        | python to_json.py \
        | jq
"""

import json
import sys
from io import StringIO
from pathlib import Path

import lark
import rich
from metovlogs import get_log

import lib

log = get_log(__name__, default_level="INFO")


def main():
    raw = sys.stdin.read()
    data = parse_data(raw)
    json.dump(data, sys.stdout)


def parse_data(raw: str) -> dict:
    p = Path(__file__).parent / "grammar.txt"
    log.debug(f"Loading grammar from: {p.absolute()}")

    grammar = p.read_text()
    try:
        parser = lark.Lark(grammar, start="dict")
    except lark.exceptions.LarkError as e:
        log.critical(f"Couldn't parse grammar:\n{e}")
        exit(1)

    try:
        ast = parser.parse(raw)
    except lark.exceptions.LarkError as e:
        log.critical(f"Couldn't parse data:\n{e}")
        exit(1)

    log.debug(f"AST:\n{render_tree(ast)}")

    data = lib.TreeToDict().transform(ast)
    log.debug(f"Parsed:\n{data}")

    return data


def render_tree(t: lark.ParseTree) -> str:
    s = StringIO()
    rich.print(t, file=s)
    return s.getvalue()


if __name__ == "__main__":
    main()
