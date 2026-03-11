#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BASE="$ROOT/.codex"

required=(
  "$BASE/rules/WORKSPACE_RULES_GLOBAL.md"
  "$BASE/skills/doc25-orchestrator/SKILL.md"
  "$BASE/skills/doc25-init/SKILL.md"
  "$BASE/skills/doc25-dev-workflow/SKILL.md"
  "$BASE/skills/doc25-docs-workflow/SKILL.md"
  "$BASE/skills/doc25-commit-gate/SKILL.md"
  "$BASE/skills/doc25-rules-policy/SKILL.md"
)

for f in "${required[@]}"; do
  [ -f "$f" ] || { echo "missing: $f"; exit 1; }
done

for skill in "$BASE/skills"/*; do
  [ -d "$skill" ] || continue
  [ -f "$skill/SKILL.md" ] || { echo "missing SKILL.md in $skill"; exit 1; }
  grep -q '^---' "$skill/SKILL.md" || { echo "invalid frontmatter in $skill/SKILL.md"; exit 1; }
done

echo "codex stack validation: OK"
