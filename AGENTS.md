# broccoli-rish agent operating contract

One capability. One physical wrapper owned by broccoli-core. One live probe.

You are editing the **Android Rish/Shizuku transport**. You are not editing OmniKali desktop, Grasshopper task lifecycle, Helix, MCP, or Broccoli history.

## Read this, then stop expanding context

1. This file.
2. `README.md` if the task is unfamiliar.
3. `PROVENANCE.md` before changing extracted files.
4. The single file you are changing.

Do not copy or ingest broccoli-core. Refer to its installed canonical wrapper.

## Map

- Physical execution owner: `$HOME/broccoli-core/lib/rish_run.sh`
- Compatibility redirect: `lib/rish_run.sh`
- Python bridge: `tools/android_transport.py` (`RishTransport`)
- RDC/background re-entry: `tools/termux_run_command.py`
- Live probe: `lib/rish_transport_probe.sh` → `tools/rish_transport_probe.py`
- Offline tests: `tests/test_fail_closed.py`, `tests/test_probe_contract.py`

## Invariants (do not “fix” these)

- `RISH_PRESERVE_ENV=0`
- fail closed: empty command → 2, missing core → 78; core preserves missing env → 78, missing binary → 79
- RC=0 with empty output is not PASS
- `termux_run_command` is not a second Rish; it only moves the caller into Termux so `rish_run.sh` can run
- executor stays on the phone

## Verify

```text
python3 -m unittest discover -s tests -t . -v
```

Live uid=2000 is required before claiming PROVEN:

```text
RISH_PRESERVE_ENV=0 bash ./lib/rish_transport_probe.sh
```

If you cannot run on the phone, leave status NOT_PROVEN and do not invent evidence.

## Stop and ask if

- the change would add a second wrapper
- the change would edit Helix, Grasshopper control plane, or broccoli-core history
- the change would promote this repo to PROVEN without live uid=2000 output
- the change would create `broccoli-mcp` (that is M3, gated)
