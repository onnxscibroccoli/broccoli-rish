#!/usr/bin/env python3
"""Offline contract tests for the live probe. No Android required."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.rish_transport_probe import (
    ProbeResult,
    build_probe_command,
    run_probe,
    validate_output_path,
)


class FakeTransport:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.commands = []

    def run(self, command, timeout=None):
        self.commands.append(command)
        return ProbeResult  # placeholder, replaced below


class Result:
    def __init__(self, returncode, stdout, stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class RecordingTransport:
    def __init__(self, result):
        self.result = result
        self.commands = []

    def run(self, command, timeout=None):
        self.commands.append(command)
        return self.result


class ProbeContractTests(unittest.TestCase):
    def test_rejects_parent_directory(self):
        with self.assertRaises(ValueError):
            validate_output_path("/sdcard/OmniKali/../secret.txt")

    def test_rejects_non_shared_storage(self):
        with self.assertRaises(ValueError):
            validate_output_path("/tmp/proof.txt")

    def test_accepts_sdcard_path(self):
        self.assertEqual(
            validate_output_path("/sdcard/OmniKali/broccoli/rish-transport-proof.txt"),
            "/sdcard/OmniKali/broccoli/rish-transport-proof.txt",
        )

    def test_empty_output_is_not_pass(self):
        transport = RecordingTransport(Result(0, ""))
        result = run_probe(transport=transport, marker="RDC_RISH_TARGET_OK_deadbeef")
        self.assertFalse(result.ok)
        self.assertIn("target marker missing", result.error)

    def test_missing_uid_is_not_pass(self):
        transport = RecordingTransport(
            Result(0, "RDC_RISH_TARGET_OK_deadbeef\nuid=2000\n35\n")
        )
        result = run_probe(transport=transport, marker="RDC_RISH_TARGET_OK_deadbeef")
        self.assertFalse(result.ok)
        self.assertIn("Android shell identity missing", result.error)

    def test_uid2000_shell_is_required(self):
        evidence = "RDC_RISH_TARGET_OK_deadbeef\nuid=2000(shell) gid=2000(shell)\n35\n"
        transport = RecordingTransport(Result(0, evidence))
        result = run_probe(transport=transport, marker="RDC_RISH_TARGET_OK_deadbeef")
        self.assertTrue(result.ok)
        self.assertIn("uid=2000(shell)", result.evidence)

    def test_probe_command_writes_id_and_sdk(self):
        command = build_probe_command(
            "/sdcard/OmniKali/broccoli/rish-transport-proof.txt",
            "MARKER",
        )
        self.assertIn("id >>", command)
        self.assertIn("getprop ro.build.version.sdk", command)
        self.assertIn("test -s", command)


if __name__ == "__main__":
    unittest.main()
