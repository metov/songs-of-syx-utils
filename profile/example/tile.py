"""
Tile a room blueprint.

The new blueprint will be added with a new name (original with a suffix). The
old file will be backed up.

This doesn't seem to work well if Songs of Syx is already running. Close the
game first.

The tiling assumes that the outermost border is a line of walls. The walls will
be stretched instead of being duplicated.

Usage:
    tile.py BLUEPRINTS_TXT_PATH BLUEPRINT_NAME HORZ VERT

Arguments:
    BLUEPRINTS_TXT_PATH
        path to Songs of Syx "SavedPrints.txt" file

    BLUEPRINT_NAME
        exact name of blueprint to tile

    HORZ
        how many times to tile horizontally

    VERT
        how many times to tile vertically
"""

from datetime import datetime
import shutil
import sys
from pathlib import Path

from docopt import docopt
from metovlogs import get_log
from rich import print

# Import modules from parent dir
sys.path.append(str(Path(__file__).parent.parent))
import from_json
import to_json

log = get_log(
    __name__,
    # default_level="INFO",
)


def main():
    args = docopt(__doc__)
    p = Path(args["BLUEPRINTS_TXT_PATH"])
    raw = p.read_text()
    data = to_json.parse_data(raw)

    name = args["BLUEPRINT_NAME"]
    try:
        d = dict(next(d for d in data["BLUEPRINTS"] if d["NAME"] == name))
    except StopIteration:
        log.critical(f"Couldn't find blueprint: {name}")
        exit(1)
    m = get_mat(d)
    log.debug(f"Original blueprint:\n{render_mat(m)}")

    try:
        horz = int(args["HORZ"])
        vert = int(args["VERT"])
    except ValueError:
        log.critical(f"HORZ and VERT must be integers.")
        exit(1)

    tile_right(m, horz - 1)
    tile_down(m, vert - 1)
    log.debug(f"Tiled blueprint:\n{render_mat(m)}")

    d["NAME"] += f" t{horz}x{vert}"
    if any(d["NAME"] == x["NAME"] for x in data["BLUEPRINTS"]):
        log.warning(f"Blueprint will be overwritten: {d['NAME']}")
    set_mat(d, m)

    data["BLUEPRINTS"] += [d]
    syx = from_json.render_data(data)
    backup_file(p)
    p.write_text(syx)


def get_mat(d: dict):
    data = d["DATA"]
    width = d["WIDTH"]
    height = d["HEIGHT"]
    assert width * height == len(data)

    m = []
    for i, x in enumerate(data):
        if i % width == 0:
            u = []
            m += [u]

        u += [x]

    return m


def render_mat(m: list[list[int]]) -> str:
    width = max(max(len(str(i)) for i in u) for u in m)
    s = "\n".join("".join(str(i).rjust(width + 1) for i in row) for row in m)
    return s


def tile_right(m: list[list[int]], n: int):
    for row in m:
        for i in row[1:-1] * n:
            row.insert(len(row) - 1, i)


def tile_down(m: list[list[int]], n: int):
    for row in m[1:-1] * n:
        m.insert(len(m) - 1, list(row))


def set_mat(d: dict, m: list[list[int]]):
    d["WIDTH"] = len(m[0])
    d["HEIGHT"] = len(m)
    d["DATA"] = sum(m, start=[])


def backup_file(p: Path):
    new_stem = f"{p.stem}-{datetime.now():%Y%m%d-%H%M%S}"
    pb = p.with_stem(new_stem)
    log.info(f"Backing up old file to {pb}")
    shutil.copy(p, p.with_stem(p.stem + "-backup"))


if __name__ == "__main__":
    main()
