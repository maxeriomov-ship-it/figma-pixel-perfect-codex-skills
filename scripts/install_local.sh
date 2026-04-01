#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$TARGET_DIR"
cp -R "$ROOT_DIR/skills/figma-pixel-perfect-web" "$TARGET_DIR/"
cp -R "$ROOT_DIR/skills/figma-pixel-perfect-ios" "$TARGET_DIR/"
cp -R "$ROOT_DIR/skills/figma-pixel-perfect-router" "$TARGET_DIR/"

echo "Installed skills to: $TARGET_DIR"
echo "- figma-pixel-perfect-web"
echo "- figma-pixel-perfect-ios"
echo "- figma-pixel-perfect-router"
