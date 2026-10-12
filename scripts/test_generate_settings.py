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


if __name__ == "__main__":
    unittest.main()
