# broccoli-rish

**Capability owner:** Android Rish/Shizuku transport  
**Status:** EXTRACTED / NOT_PROVEN against this repository  
**Source archive:** [`broccoli-core`](https://github.com/onnxscibroccoli/broccoli-core) @ `95041af6e0acb75e5c03363e2becf13b959d0e96`

This repository is the agent-sized surface for one capability: get a command from Termux or an RDC/background child into Android shell `uid=2000` through the canonical wrapper.

It is **not** a desktop, not an MCP server, not a second `rish` binary, and not a cleanup of Broccoli history.

## Frozen contract

```
RDC/Termux -> RishTransport -> lib/rish_run.sh -> Rish/Shizuku -> Android shell uid=2000
```

Invariants:

- One wrapper: `lib/rish_run.sh`. Do not add another.
- `RISH_PRESERVE_ENV=0` remains the invocation invariant.
- Do not persist the whole Termux environment.
- RC=0 with empty output is not PASS.
- The executor stays on the phone. A workstation process must not impersonate it.
- `lib/rish_run.py` from broccoli-core is a competing historical wrapper. It is **not** extracted here.

## Agent surface

Read `AGENTS.md` first. Provenance is in `PROVENANCE.md`.

| Path | Role |
|---|---|
| `lib/rish_run.sh` | Canonical wrapper |
| `tools/android_transport.py` | `RishTransport` |
| `tools/termux_run_command.py` | RDC/background bridge into Termux. Not a second transport. |
| `lib/rish_transport_probe.sh` | Live fail-closed probe |
| `tools/rish_transport_probe.py` | Probe implementation |
| `tests/test_fail_closed.py` | Offline negative gates |

## Tests

Offline (CI / any Linux bash):

```bash
python3 -m unittest discover -s tests -t . -v
```

Live (Android/Termux only; this is the uid=2000 proof):

```bash
RISH_PRESERVE_ENV=0 bash ./lib/rish_transport_probe.sh
```

Live PASS requires `uid=2000(shell)` in the evidence and a non-empty artifact. Until that retest is recorded against **this** repo, status stays NOT_PROVEN here even though broccoli-core previously passed the same files.

Historical live evidence (broccoli-core, not this repo):

```text
RISH_PRESERVE_ENV=0 bash ./lib/rish_run.sh 'echo BROCCOLI_RISH_OK; id; getprop ro.build.version.sdk'
BROCCOLI_RISH_OK
uid=2000(shell) ...
35
exit 0
```

Negative gates (must keep):

- no command → exit 2
- missing runtime environment → exit 78
- missing Rish binary → exit 79

## Consumers

- Grasshopper Android client consumes this transport. It must not own Rish.
- broccoli-core remains the archive and still contains the original files.
- `broccoli-mcp` is not extracted until this repo has live uid=2000 evidence.

## Forbidden

- rewriting the wrapper because a new caller failed
- copying Broccoli mirrors, logs, Word docs, or APKs into this repo
- claiming production desktop or RDC end-to-end proof from a transport identity proof
- mutating Helix / CloudFront / nginx / 80 / 443
