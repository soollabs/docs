#!/usr/bin/env python3
"""Read the HMD release tag pinned in the documentation renderer workflow."""

import argparse
from pathlib import Path
import re


def renderer_ref(path):
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "renderer-ref:":
            continue
        indent = len(line) - len(line.lstrip())
        for child in lines[index + 1:]:
            if child.strip() and len(child) - len(child.lstrip()) <= indent:
                break
            if not child.strip().startswith("default:"):
                continue
            value = child.strip().removeprefix("default:").split("#", 1)[0].strip()
            if value.startswith(("'", '"')) and value.endswith(value[0]):
                value = value[1:-1]
            if re.fullmatch(r"v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", value):
                return value
        raise ValueError("renderer-ref must pin a release tag such as v0.3.0")
    raise ValueError("renderer-ref input is missing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path, nargs="?", default=Path(".github/workflows/_render-static-docs.yml"))
    args = parser.parse_args()
    print(renderer_ref(args.workflow))
