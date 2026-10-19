#!/usr/bin/env python3
"""Generate Markdown settings and MCP tool tables from a released HMD checkout."""

import argparse
import json
import re
from pathlib import Path


STORES = {
    "config": "reference/configuration.md",
    "wiki": "reference/wiki-configuration.md",
    "namespace": "reference/namespace-configuration.md",
    "preferences": "admin/settings.md",
}

MCP_PAGE = "reference/mcp-tools.md"


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


# Wiki-links and Markdown links in a tool description are examples, not links:
# code spans keep the docs site from rendering them.
LINK_SYNTAX = re.compile(r"\[\[[^\]]*\]\]|!?\[[^\]]*\]\([^)]*\)")


def text(value):
    escaped = cell(value).replace("<", "&lt;").replace(">", "&gt;")
    return LINK_SYNTAX.sub(lambda match: "`" + match.group(0) + "`", escaped)


def effect(annotations):
    # MCP defaults: a tool is not read-only and is destructive unless it says otherwise.
    if annotations.get("readOnlyHint"):
        return "read-only"
    return "destructive" if annotations.get("destructiveHint", True) else "writes"


def tool_summary(tools):
    lines = [
        "| Tool | Scope | Effect | What it does |",
        "| --- | --- | --- | --- |",
    ]
    for tool in tools:
        description = text(tool["description"])
        if tool.get("x-document-search"):
            description += " Listed only when document search is enabled."
        lines.append("| " + " | ".join((
            "`" + tool["name"] + "`", tool["x-scope"], effect(tool.get("annotations", {})), description,
        )) + " |")
    return "\n".join(lines)


def parameter_rules(schema):
    parts = [] if rules(schema) == "—" else [rules(schema)]
    if "x-default" in schema:
        parts.append("default: " + literal(schema["x-default"]))
    if schema.get("properties"):
        parts.append("fields: " + ", ".join("`" + key + "`" for key in schema["properties"]))
    return "; ".join(parts) or "—"


def tool_parameters(tools):
    sections = []
    for tool in tools:
        schema = tool["inputSchema"]
        heading = "### `" + tool["name"] + "`"
        properties = schema.get("properties", {})
        if not properties:
            sections.append(heading + "\n\nNo parameters.")
            continue
        required = set(schema.get("required", []))
        lines = [
            heading, "",
            "| Parameter | Type | Required | Accepted values | Description |",
            "| --- | --- | --- | --- | --- |",
        ]
        for key, parameter in properties.items():
            if not parameter.get("description"):
                raise ValueError(f"{tool['name']}.{key} has no description")
            lines.append("| " + " | ".join((
                "`" + key + "`", cell(parameter.get("type", "unspecified")),
                "Yes" if key in required else "No", parameter_rules(parameter),
                text(parameter["description"]),
            )) + " |")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def replace_block(path, body, name, content):
    start, end = f"<!-- generated:{name} -->", f"<!-- /generated:{name} -->"
    if body.count(start) != 1 or body.count(end) != 1:
        raise ValueError(f"{path}: expected exactly one {name} marker pair")
    before, rest = body.split(start)
    previous, after = rest.split(end)
    if end in before:
        raise ValueError(f"{path}: reversed {name} markers")
    return before + start + "\n\n" + content + "\n\n" + end + after


def generate(schema_dir, docs_dir, mcp_tools=None):
    # Validate all inputs before changing any output.
    updates = []
    for store, relative in STORES.items():
        schema = json.loads((schema_dir / (store + ".schema.json")).read_text())
        path = docs_dir / relative
        updates.append((path, replace_block(path, path.read_text(), store, table(store, schema))))
    if mcp_tools is not None:
        tools = json.loads(mcp_tools.read_text())
        path = docs_dir / MCP_PAGE
        body = replace_block(path, path.read_text(), "mcp-tools", tool_summary(tools))
        updates.append((path, replace_block(path, body, "mcp-parameters", tool_parameters(tools))))
    for path, body in updates:
        if path.read_text() != body:
            path.write_text(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-dir", type=Path, required=True)
    parser.add_argument("--mcp-tools", type=Path, help="internal/mcp/schema/tools.json from the same HMD release")
    parser.add_argument("--docs-dir", type=Path, default=Path("holdmydocs"))
    args = parser.parse_args()
    generate(args.schema_dir, args.docs_dir, args.mcp_tools)
