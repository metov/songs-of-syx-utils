"""
Convert JSON to a Songs of Syx datagram.

Example:
    cat SavedProfiles.json | python from_json.py
"""

import json
import string
import sys
import textwrap

from metovlogs import get_log

log = get_log(__name__, default_level="INFO")


def main():
    data = json.load(sys.stdin)
    syx = render_data(data)
    sys.stdout.write(syx)


def render_data(data: dict):
    syx = render_dict(data)
    return syx.replace("\n", "\r\n")


def render_dict(d: dict) -> str:
    lines = []
    for k, v in d.items():
        s = f"{k}: {render_value(v)},\n"
        lines += [s]
    return "".join(lines)


def render_list(u: list) -> str:
    lines = []
    for i in u:
        lines += [f"{render_value(i)},"]
    return "\n".join(lines)


def render_value(v) -> str:
    if isinstance(v, dict):
        return "{\n" + render_dict(v) + "\n}"
    if isinstance(v, list):
        return "[\n" + textwrap.indent(render_list(v), "\t") + "\n\t]"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return render_string(v)
    else:
        log.error(f"Unexpected type: {type(v)}")
        return str(v)


def render_string(s) -> str:
    u = string.ascii_uppercase + "_"
    if all(c in u for c in s):
        return s

    return f'"{s}"'


if __name__ == "__main__":
    main()
