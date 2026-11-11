# Portfolio reviewer readiness — broccoli-rish

**Focus:** Isolated Android Rish/Shizuku non-root transport  
**Current evidence status:** `EXTRACTED / LIVE_NOT_PROVEN_HERE` (2026-11-11 snapshot; **not** production approval).  
**Tracking:** [repository issue](https://github.com/onnxscibroccoli/broccoli-rish/issues/2) · [portfolio master ledger](https://github.com/onnxscibroccoli/broccoli-core/issues/102)  


## Inspect actual source
- [lib/rish_run.sh](https://github.com/onnxscibroccoli/broccoli-rish/blob/main/lib/rish_run.sh)
- [tools/android_transport.py](https://github.com/onnxscibroccoli/broccoli-rish/blob/main/tools/android_transport.py)
- [tests/test_fail_closed.py](https://github.com/onnxscibroccoli/broccoli-rish/blob/main/tests/test_fail_closed.py)

**Scoped reference workflow run:** [Inspect the historical GitHub Actions result](https://github.com/onnxscibroccoli/broccoli-rish/actions/runs/37240938647). Verify its SHA/branch before attributing it to current source; CI success is not live/production evidence.
Recorded 2026-11-11: run 37240938647 is the `fail-closed` workflow on a `push` to `main` at `0218a9a39a33ae0b5343c1051c537ffa36544819` (the current `main` head), conclusion success. It covers the offline unittest suite only (11 tests), not a device.

## First reviewer command (check prerequisites before executing)

```sh
python3 -m unittest discover -s tests -t . -v
```

This is a proposed reproduction command, **not a claim of executed testing**. Confirm the command exists in the current repository; record missing scripts/dependencies as NOT_VERIFIED rather than masking failures.

## Ordered implementation queue

1. [ ] Link canonical Rish wrapper and fail-closed offline tests to a minimal 10-minute transport demo.
2. [ ] Keep historical uid=2000 evidence separate from current repo live verification.
3. [ ] Record a fresh authorized device uid=2000 proof with nonempty output and explicit Android permission requirements.
4. [ ] Package only transport contract and minimal integration usage; no false desktop claim.

## Evidence promotion gate

A project is not ready for a public professional demonstration merely because it has a README, an Actions schedule, or a test result unrelated to its claimed behavior. Provide exact source SHA, real test scope, negative controls, and meaningful limitations. Production or hardware assertions require an authorized real environment and appropriately scoped acceptance.

## Safe resumption

Inspect this issue and the master ledger, refresh the repo's `main` head and relevant PRs, implement the first unchecked item on a draft PR, attach exact test evidence and update the tracker. Avoid mass merging, secret exposure, false human review, and speculative employment claims.
