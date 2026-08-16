#!/bin/bash
# load-hq-context.sh — Inject Rob's HQ hub context (rocap1982/hq) at session start.
#
# Canonical copy lives in rocap1982/hq/hooks/. Install into any repo by copying
# to .claude/hooks/ and registering a SessionStart hook in .claude/settings.json
# (see hq/SYSTEM.md — "The auto-load hook").
#
# Behaviour:
#   - Finds an hq clone in known locations (remote workspace, Rob's PC, sibling dir)
#   - Refreshes it quietly (10s cap — never blocks session start)
#   - Prints personal/robert.md + INDEX.md so every session starts knowing who
#     Rob is, how to work with him, and where all context lives
#   - No clone found → prints an instruction to add_repo rocap1982/hq instead
#
# Exit 0 always — context loading must never fail a session.

set -u

CANDIDATES=(
  "/workspace/hq"
  "/c/dev/hq"
  "C:/dev/hq"
  "$HOME/dev/hq"
  "$HOME/hq"
)
if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
  CANDIDATES+=("$CLAUDE_PROJECT_DIR/../hq")
fi

HQ_DIR=""
for d in "${CANDIDATES[@]}"; do
  if [ -f "$d/INDEX.md" ]; then
    HQ_DIR="$d"
    break
  fi
done

if [ -z "$HQ_DIR" ]; then
  echo "HQ hub (rocap1982/hq) not present locally. Before substantive work: add it to the session (add_repo rocap1982/hq), then read INDEX.md and personal/robert.md — they carry Rob's identity, standing rules, and the map of every repo. Durable cross-company/personal facts learned this session get committed back to hq main before close (see hq/SYSTEM.md)."
  exit 0
fi

# Best-effort refresh — quiet, capped, never blocks startup.
if command -v timeout >/dev/null 2>&1; then
  timeout 10 git -C "$HQ_DIR" pull --ff-only --quiet >/dev/null 2>&1 || true
else
  git -C "$HQ_DIR" pull --ff-only --quiet >/dev/null 2>&1 || true
fi

echo "=== HQ HUB CONTEXT (auto-loaded from $HQ_DIR) ==="
echo "This is Rob's master context system. Treat the two files below as read."
echo
echo "--- personal/robert.md ---"
cat "$HQ_DIR/personal/robert.md" 2>/dev/null
echo
echo "--- INDEX.md (map of all repos) ---"
cat "$HQ_DIR/INDEX.md" 2>/dev/null
echo
echo "=== END HQ HUB CONTEXT ==="
echo "Standing obligation: durable cross-company or personal facts learned this session are committed to hq main before session close (see hq/SYSTEM.md). Romark client/job judgment goes to Romark-workle/docs/romark-knowledge/ instead."
exit 0
