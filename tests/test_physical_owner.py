import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.android_transport import RishTransport

ROOT = Path(__file__).resolve().parents[1]

class PhysicalOwnerTests(unittest.TestCase):
    def test_physical_default_is_broccoli_core_wrapper(self):
        with patch.dict(os.environ, {'HOME': '/tmp/phone-home'}, clear=True):
            transport = RishTransport()
        self.assertEqual(transport.wrapper, '/tmp/phone-home/broccoli-core/lib/rish_run.sh')

    def test_explicit_remote_wrapper_is_preserved(self):
        self.assertEqual(RishTransport('/custom/remote.sh').wrapper, '/custom/remote.sh')

    def test_extracted_shell_entrypoint_delegates_to_core_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = Path(tmp) / 'broccoli-core/lib'
            core.mkdir(parents=True)
            (core / 'rish_run.sh').write_text('#!/bin/bash\nprintf "CORE:%s\\n" "$*"\nexit 23\n')
            env = dict(os.environ, HOME=tmp)
            result = subprocess.run(['bash', str(ROOT / 'lib/rish_run.sh'), 'echo "a b"; id'], env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 23, result.stderr)
            self.assertEqual(result.stdout, 'CORE:echo "a b"; id\n')

    def test_missing_core_never_uses_raw_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / 'raw-rish'
            raw.write_text('#!/bin/sh\nprintf RAW_SHOULD_NOT_RUN\n')
            raw.chmod(0o700)
            result = subprocess.run(['bash', str(ROOT / 'lib/rish_run.sh'), 'id'], env=dict(os.environ, HOME=tmp, BROCCOLI_RISH_BIN=str(raw)), text=True, capture_output=True)
            self.assertEqual(result.returncode, 78)
            self.assertNotIn('RAW_SHOULD_NOT_RUN', result.stdout)

if __name__ == '__main__': unittest.main()
