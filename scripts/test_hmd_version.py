"""Check that schema generation uses the renderer's pinned release."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("version", Path(__file__).with_name("hmd-version.py"))
version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version)


class VersionTests(unittest.TestCase):
    def parse(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "workflow.yml"
            path.write_text(text)
            return version.renderer_ref(path)

    def test_release_pin(self):
        for value in ["v0.3.0", "'v0.4.0'", '"v0.5.0-rc.1"']:
            with self.subTest(value=value):
                self.assertEqual(self.parse(
                    "inputs:\n  other:\n    default: ignore\n"
                    "  renderer-ref:\n    description: HMD version\n"
                    "    # renovate: datasource=github-tags\n"
                    f"    default: {value} # pinned\n    type: string\n"
                ), value.strip("'\""))

    def test_missing_or_non_release_pin(self):
        for text in [
            "inputs:\n  other:\n    default: v0.3.0\n",
            "inputs:\n  renderer-ref:\n    default: main\n",
            "inputs:\n  renderer-ref:\n    default: 'v0.3.0\n",
            "inputs:\n  renderer-ref:\n    type: string\n  other:\n    default: v0.3.0\n",
        ]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.parse(text)

    def test_workflow_uses_pin_with_unprivileged_pr_checks(self):
        workflow = Path(__file__).resolve().parents[1] / ".github/workflows/update-settings-reference.yml"
        text = workflow.read_text()
        for expected in (
            "pull_request:", "schedule:", "branches: [main]",
            '".github/workflows/_render-static-docs.yml"',
            "python3 scripts/hmd-version.py",
            "ref: ${{ steps.version.outputs.tag }}",
            "github.event_name != 'pull_request'",
            "github.ref == 'refs/heads/main'",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("releases/latest", text)
        self.assertNotIn("repository_dispatch", text)
        generate = text.split("  generate:\n", 1)[1].split("  propose:\n", 1)[0]
        self.assertNotIn("contents: write", generate)
        self.assertNotIn("git push", generate)


if __name__ == "__main__":
    unittest.main()
