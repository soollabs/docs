#!/usr/bin/env python3
"""Generate Markdown settings tables from a released HMD schema directory."""

import argparse
import json
from pathlib import Path


STORES = {
    "config": "reference/configuration.md",
    "wiki": "reference/wiki-configuration.md",
    "namespace": "reference/namespace-configuration.md",
    "preferences": "admin/settings.md",
}


def cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ").replace("\r", "")


def literal(value):
    return "`" + cell(json.dumps(value, ensure_ascii=False)) + "`"


def rules(schema):
    parts = []
    if "enum" in schema:
        parts.append(", ".join(literal(value) for value in schema["enum"]))
    if "oneOf" in schema:
        for option in schema["oneOf"]:
            if "const" not in option:
                raise ValueError("oneOf options must have const values")
            parts.append(literal(option["const"]) + (
                " (" + cell(option["title"]) + ")" if "title" in option else ""
            ))
    for key, label in (
        ("pattern", "pattern"), ("format", "format"),
        ("minimum", "minimum"), ("maximum", "maximum"),
        ("minLength", "minimum length"), ("maxLength", "maximum length"),
        ("minItems", "minimum items"), ("maxItems", "maximum items"),
    ):
        if key in schema:
            parts.append(label + ": " + literal(schema[key]))
    if "x-schemes" in schema:
        parts.append("schemes: " + ", ".join(literal(v) for v in schema["x-schemes"]))
    if schema.get("uniqueItems"):
        parts.append("unique items")
    if "items" in schema:
        item = schema["items"]
        item_rules = rules(item)
        parts.append("items: " + cell(item.get("type", "unspecified")) + (
            "; " + item_rules if item_rules != "—" else ""
        ))
        if item.get("properties"):
            for key, child in item["properties"].items():
                parts.append("item `" + cell(key) + "`: " + rules(child))
        if item.get("required"):
            parts.append("required item fields: " + ", ".join(item["required"]))
    return "; ".join(parts) or "—"


def leaves(schema, prefix=""):
    for key, value in schema.get("properties", {}).items():
        path = prefix + key
        if value.get("type") == "object" and value.get("properties"):
            yield from leaves(value, path + ".")
        else:
            yield path, value


def table(store, schema):
    lines = [
        "| Key | Environment variable | Type and default | Accepted values | Restart | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for path, setting in leaves(schema):
        if not setting.get("description"):
            raise ValueError(f"{store}.{path} has no description")
        env = setting.get("x-env")
        if env is None and store == "config" and setting.get("type") != "array":
            env = "HMD_" + path.upper().replace(".", "_")
        key = "`" + path + "`"
        if setting.get("x-env-only"):
            key += " (environment only; not a file key)"
        kind = cell(setting.get("type", "unspecified"))
        kind += ", " + literal(setting["default"]) if "default" in setting else "; not specified"
        restart = ("Yes" if setting["x-restart"] else "No") if "x-restart" in setting else "—"
        description = cell(setting["description"]).replace("<", "&lt;").replace(">", "&gt;")
        if setting.get("x-secret"):
            description += " **Secret.**"
        lines.append("| " + " | ".join((
            key, "`" + env + "`" if env else "—", kind,
            rules(setting), restart, description,
        )) + " |")
    return "\n".join(lines)


def generate(schema_dir, docs_dir):
    # Validate all inputs before changing any output.
    updates = []
    for store, relative in STORES.items():
        schema = json.loads((schema_dir / (store + ".schema.json")).read_text())
        path = docs_dir / relative
        body = path.read_text()
        start, end = f"<!-- generated:{store} -->", f"<!-- /generated:{store} -->"
        if body.count(start) != 1 or body.count(end) != 1:
            raise ValueError(f"{path}: expected exactly one marker pair")
        before, rest = body.split(start)
        previous, after = rest.split(end)
        if end in before:
            raise ValueError(f"{path}: reversed markers")
        updates.append((path, before + start + "\n\n" + table(store, schema) + "\n\n" + end + after))
    for path, body in updates:
        if path.read_text() != body:
            path.write_text(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-dir", type=Path, required=True)
    parser.add_argument("--docs-dir", type=Path, default=Path("holdmydocs"))
    args = parser.parse_args()
    generate(args.schema_dir, args.docs_dir)
