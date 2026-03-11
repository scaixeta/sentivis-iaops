#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$REPO_ROOT/.codex/skills"
DEST="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$DEST"

for d in "$SRC"/*; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  rm -rf "$DEST/$name"
  cp -R "$d" "$DEST/$name"
  echo "synced: $name"
done

echo "sync complete: $SRC -> $DEST"
