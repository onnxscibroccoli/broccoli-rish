# broccoli-rish

**Capability:** Consumer bridge for Android transport.
**Status:** Offline tests pass; exact-commit phone/R2 verification NOT_PROVEN.

Physical Android has one execution owner: `broccoli-core/lib/rish_run.sh`.
This repository no longer maintains a competing physical launch path. Its
`lib/rish_run.sh` is a compatibility redirect into the installed broccoli-core
checkout; the exported Shizuku `rish` launcher remains an internal dependency of
that core wrapper. Do not invoke it directly or delete its DEX.

```
RDC/Termux -> RishTransport -> broccoli-core/lib/rish_run.sh -> Shizuku -> uid=2000
```

## Configuration

Install the core checkout at `$HOME/broccoli-core`, or set `BROCCOLI_CORE_ROOT`
to the correct core checkout. The physical default always resolves that checkout's
`lib/rish_run.sh`. Missing core returns an error instead of raw Rish or host shell.
Commands, nonzero exit statuses, and `RISH_PRESERVE_ENV=0` are preserved.

For an explicitly selected remote/cloud Android transport, callers may provide
`RishTransport(wrapper="/path/to/remote-wrapper.sh")`. Remote wrapper selection is
explicit; physical failures do not silently switch devices or providers.

The RDC/background Termux bridge changes calling context only. It does not own a
second Rish transport. The physical executor stays on the phone.

## Tests

```bash
python3 -m unittest discover -s tests -t . -v
```

Fourteen offline tests cover ownership, a customized remote wrapper, missing core,
exit propagation, intact quoted commands, and the evidence contract. RC=0 with empty
output is not PASS. A fresh live probe against this exact commit is still required:

```bash
RISH_PRESERVE_ENV=0 bash ./lib/rish_transport_probe.sh
```

Live PASS requires `uid=2000(shell)`, the current unique marker, and a nonempty proof
artifact. Historical core proof does not establish this checkout's R2 acceptance.

Read `AGENTS.md` and `PROVENANCE.md` before editing. No MCP extraction or production
promotion is implied by this ownership correction.
