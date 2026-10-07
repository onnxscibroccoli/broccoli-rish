#!/data/data/com.termux/files/usr/bin/bash
# Physical transport is owned by broccoli-core; this file is only a redirect.
set -euo pipefail
CMD="$*"
[ -n "$CMD" ] || { echo "usage: rish_run.sh <shell-cmd>" >&2; exit 2; }
CORE="${BROCCOLI_CORE_ROOT:-$HOME/broccoli-core}"
WRAPPER="$CORE/lib/rish_run.sh"
[ -r "$WRAPPER" ] || { echo "RISH_CORE_WRAPPER_MISSING: $WRAPPER" >&2; exit 78; }
export RISH_PRESERVE_ENV=0
exec bash "$WRAPPER" "$CMD"
