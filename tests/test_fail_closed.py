"""Offline gates for the extracted entrypoint; low-level gates belong to core."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

WRAPPER = Path(__file__).resolve().parents[1] / 'lib/rish_run.sh'

class FailClosedTests(unittest.TestCase):
    def test_missing_command_exits_2(self):
        result = subprocess.run(['bash', str(WRAPPER)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('usage:', result.stderr)

    def test_missing_core_exits_78(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(['bash', str(WRAPPER), 'id'], capture_output=True, text=True, env=dict(os.environ, BROCCOLI_CORE_ROOT=tmp))
        self.assertEqual(result.returncode, 78)
        self.assertIn('RISH_CORE_WRAPPER_MISSING', result.stderr)

    def test_core_failure_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            lib = Path(tmp) / 'lib'
            lib.mkdir()
            (lib / 'rish_run.sh').write_text('#!/bin/sh\necho RISH_BIN_MISSING >&2\nexit 79\n')
            result = subprocess.run(['bash', str(WRAPPER), 'id'], capture_output=True, text=True, env=dict(os.environ, BROCCOLI_CORE_ROOT=tmp))
        self.assertEqual(result.returncode, 79)
        self.assertIn('RISH_BIN_MISSING', result.stderr)

if __name__ == '__main__': unittest.main()
