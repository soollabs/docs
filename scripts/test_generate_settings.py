"""Offline tests for the schema-to-Markdown generator."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("generator", Path(__file__).with_name("generate-settings.py"))
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class GeneratorTests(unittest.TestCase):
    def test_mcp_defaults(self):
        for value in (0, False, "", 40000):
            with self.subTest(value=value):
                self.assertEqual(
                    "default: " + generator.literal(value),
                    generator.parameter_rules({"x-default": value}),
                )
        self.assertEqual("—", generator.parameter_rules({}))

    def test_workflow_mcp_schema_path(self):
        workflow = (Path(__file__).resolve().parents[1] /
                    ".github/workflows/update-settings-reference.yml").read_text()
        self.assertEqual(2, workflow.count(".schema-source/internal/mcp/schema/tools.json"))
        self.assertNotIn(".schema-source/internal/mcp/tools.json", workflow)

    def test_metadata_and_rules(self):
        schema = {"properties": {"git": {"type": "object", "properties": {
            "sync_mode": {"type": "string", "default": "push", "description": "Push | pull\nsafely.",
                          "x-restart": False, "oneOf": [{"const": "push", "title": "Push"}]},
            "token": {"type": "string", "description": "Token.", "x-env-only": True,
                      "x-env": "HMD_GIT_TOKEN", "x-secret": True},
            "list": {"type": "array", "description": "Values.", "items": {
                "type": "string", "format": "cidr"}},
        }}}}
        result = generator.table("config", schema)
        for expected in ("HMD_GIT_SYNC_MODE", "`HMD_GIT_TOKEN`", "**Secret.**",
                         "environment only; not a file key", r"Push \| pull safely.",
                         '`"push"` (Push)', "items: string; format:", "| No |"):
            self.assertIn(expected, result)
        self.assertNotIn("HMD_GIT_LIST", result)
        self.assertNotIn("HMD_", generator.table("wiki", {
            "properties": {"name": {"type": "string", "description": "Name."}}}))

    def test_missing_description(self):
        with self.assertRaises(ValueError):
            generator.table("config", {"properties": {"bad": {"type": "string"}}})

    def test_markers_and_idempotence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for store, relative in generator.STORES.items():
                (root / (store + ".schema.json")).write_text(json.dumps({
                    "properties": {"value": {"type": "boolean", "default": False, "description": "A value."}}
                }))
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"Before\n<!-- generated:{store} -->\nold\n<!-- /generated:{store} -->\nAfter\n")
            generator.generate(root, root)
            snapshot = {relative: (root / relative).read_text() for relative in generator.STORES.values()}
            generator.generate(root, root)
            for relative, body in snapshot.items():
                self.assertEqual(body, (root / relative).read_text())
                self.assertTrue(body.startswith("Before\n"))
                self.assertTrue(body.endswith("\nAfter\n"))
            (root / generator.STORES["preferences"]).write_text("No markers")
            with self.assertRaises(ValueError):
                generator.generate(root, root)
            self.assertEqual(snapshot[generator.STORES["config"]], (root / generator.STORES["config"]).read_text())


    def test_mcp_tools(self):
        tools = [
            {"x-scope": "read", "name": "search", "description": "Find <mark> in [[wiki-links]].",
                "annotations": {"readOnlyHint": True}, "inputSchema": {"type": "object", "required": ["query"],
                "properties": {"query": {"type": "string", "minLength": 1, "description": "query"},
                               "limit": {"type": "integer", "minimum": 1, "maximum": 50, "x-default": 20, "description": "hits"}}}},
            {"x-scope": "write", "x-document-search": True, "name": "upload", "description": "Link as ![alt](url).",
                "annotations": {"destructiveHint": False}, "inputSchema": {"type": "object", "properties": {
                    "export": {"type": "object", "description": "settings", "properties": {"base_url": {}}}}}},
            {"x-scope": "write", "name": "drop", "description": "Drop.", "inputSchema": {"type": "object"}},
        ]
        summary = generator.tool_summary(tools)
        for expected in ("| `search` | read | read-only | Find &lt;mark&gt; in `[[wiki-links]]`. |",
                         "| `upload` | write | writes | Link as `![alt](url)`. Listed only when document search is enabled. |",
                         "| `drop` | write | destructive |"):
            self.assertIn(expected, summary)
        parameters = generator.tool_parameters(tools)
        for expected in ("### `search`", "| `query` | string | Yes | minimum length: `1` | query |",
                         "| `limit` | integer | No | minimum: `1`; maximum: `50`; default: `20` | hits |",
                         "fields: `base_url`", "### `drop`\n\nNo parameters."):
            self.assertIn(expected, parameters)
        tools[0]["inputSchema"]["properties"]["query"].pop("description")
        with self.assertRaises(ValueError):
            generator.tool_parameters(tools)

    def test_mcp_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for store, relative in generator.STORES.items():
                (root / (store + ".schema.json")).write_text(json.dumps({"properties": {}}))
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"<!-- generated:{store} -->\n<!-- /generated:{store} -->\n")
            tools = root / "tools.json"
            tools.write_text(json.dumps([{"x-scope": "read", "name": "health", "description": "Report.",
                                                                     "inputSchema": {"type": "object"}}]))
            page = root / generator.MCP_PAGE
            page.write_text("A\n<!-- generated:mcp-tools -->\n<!-- /generated:mcp-tools -->\nB\n"
                            "<!-- generated:mcp-parameters -->\nold\n<!-- /generated:mcp-parameters -->\nC\n")
            generator.generate(root, root, tools)
            body = page.read_text()
            self.assertIn("| `health` | read | destructive | Report. |", body)
            self.assertIn("### `health`\n\nNo parameters.", body)
            self.assertNotIn("old", body)
            generator.generate(root, root, tools)
            self.assertEqual(body, page.read_text())
            generator.generate(root, root)
            self.assertEqual(body, page.read_text())
            page.write_text("no markers")
            with self.assertRaises(ValueError):
                generator.generate(root, root, tools)


if __name__ == "__main__":
    unittest.main()
