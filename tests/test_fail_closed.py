#!/usr/bin/env python3
"""Offline negative gates for lib/rish_run.sh.

These tests prove fail-closed behavior on any Linux bash. They do not prove
uid=2000. Live identity stays NOT_PROVEN until the phone probe is rerun.
"""
from __future__ import annotations

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "lib" / "rish_run.sh"


def run_wrapper(args, env):
    merged = os.environ.copy()
    merged.pop("BOOTCLASSPATH", None)
    merged.update(env)
    return subprocess.run(
        ["bash", str(WRAPPER), *args],
        capture_output=True,
        text=True,
        env=merged,
    )


class FailClosedTests(unittest.TestCase):
    def test_missing_command_exits_2(self):
        result = run_wrapper([], {"BROCCOLI_RISH_BIN": "/nonexistent/rish"})
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("usage:", result.stderr)

    def test_missing_binary_exits_79(self):
        result = run_wrapper(
            ["id"],
            {
                "BROCCOLI_RISH_BIN": "/nonexistent/rish",
                "BROCCOLI_RISH_ENV": "/nonexistent/android-runtime.env",
            },
        )
        self.assertEqual(result.returncode, 79, result.stderr)
        self.assertIn("RISH_BIN_MISSING", result.stderr)

    def test_missing_env_exits_78(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_bin = Path(tmp) / "rish"
            fake_bin.write_text("#!/bin/sh\nexit 0\n")
            fake_bin.chmod(fake_bin.stat().st_mode | stat.S_IEXEC)
            result = run_wrapper(
                ["id"],
                {
                    "BROCCOLI_RISH_BIN": str(fake_bin),
                    "BROCCOLI_RISH_ENV": str(Path(tmp) / "missing.env"),
                },
            )
        self.assertEqual(result.returncode, 78, result.stderr)
        self.assertIn("RISH_ENV_MISSING", result.stderr)

    def test_wrapper_file_exists(self):
        self.assertTrue(WRAPPER.is_file())


if __name__ == "__main__":
    unittest.main()
