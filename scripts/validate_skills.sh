#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS=(
  "$ROOT_DIR/skills/figma-pixel-perfect-web"
  "$ROOT_DIR/skills/figma-pixel-perfect-ios"
)

for skill in "${SKILLS[@]}"; do
  echo "Checking structure: $skill"
  test -f "$skill/SKILL.md"
  test -f "$skill/agents/openai.yaml"
  test -d "$skill/references"
  test -d "$skill/assets"
  test -d "$skill/scripts"

done

VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py"
if [[ -f "$VALIDATOR" ]]; then
  if python3 -c "import yaml" >/dev/null 2>&1; then
    for skill in "${SKILLS[@]}"; do
      echo "Running quick_validate.py for $skill"
      python3 "$VALIDATOR" "$skill"
    done
  else
    echo "Skip quick_validate.py: PyYAML is not installed in this Python environment"
  fi
else
  echo "Skip quick_validate.py: validator not found at $VALIDATOR"
fi

for skill in "${SKILLS[@]}"; do
  echo "Checking script CLIs in $skill"
  python3 "$skill/scripts/inspect_layout.py" --help >/dev/null
  python3 "$skill/scripts/verify_fonts.py" --help >/dev/null
  python3 "$skill/scripts/inspect_text_metrics.py" --help >/dev/null
done

echo "Validation passed."
