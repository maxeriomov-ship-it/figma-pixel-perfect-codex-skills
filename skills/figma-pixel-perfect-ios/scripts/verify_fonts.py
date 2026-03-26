#!/usr/bin/env python3
"""Verify iOS font source mapping, registration, and runtime usage.

Expected mapping JSON:
{
  "styles": [
    {
      "style_name": "Heading/H1",
      "expected_family": "Inter",
      "expected_face": "Inter SemiBold",
      "expected_source": "project-local",
      "expected_file": "Resources/Fonts/Inter-SemiBold.ttf",
      "expected_runtime_name": "Inter-SemiBold",
      "expected_weight": "semibold",
      "expected_style": "normal"
    }
  ]
}

Expected runtime JSON (optional but required for strict mode):
{
  "registered_fonts": ["Inter-SemiBold", "Inter-Regular"],
  "entries": [
    {
      "style_name": "Heading/H1",
      "runtime_name": "Inter-SemiBold",
      "runtime_family": "Inter",
      "runtime_face": "Inter SemiBold",
      "runtime_weight": "semibold",
      "runtime_style": "normal",
      "fallback_detected": false
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_STYLE_FIELDS = (
    "style_name",
    "expected_family",
    "expected_face",
    "expected_source",
    "expected_runtime_name",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def parse_info_plist_fonts(project_root: Path) -> set[str]:
    discovered: set[str] = set()
    for plist_path in project_root.rglob("Info.plist"):
        try:
            with plist_path.open("rb") as fh:
                obj = plistlib.load(fh)
        except Exception:  # noqa: BLE001
            continue
        ui_fonts = obj.get("UIAppFonts")
        if isinstance(ui_fonts, list):
            for value in ui_fonts:
                if isinstance(value, str) and value.strip():
                    discovered.add(value.strip())
    return discovered


def resolve_file(project_root: Path | None, path_value: str) -> Path:
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate
    if project_root is None:
        return candidate
    return project_root / candidate


def build_runtime_index(runtime: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = runtime.get("entries", [])
    if not isinstance(entries, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, dict):
            continue
        style_name = item.get("style_name")
        if isinstance(style_name, str) and style_name.strip():
            result[style_name] = item
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify exact iOS font mapping, registration, and runtime usage")
    parser.add_argument("--mapping", required=True, type=Path, help="Typography mapping JSON")
    parser.add_argument("--project-root", type=Path, default=None, help="Project root for file/plist checks")
    parser.add_argument("--runtime", type=Path, default=None, help="Runtime font report JSON")
    parser.add_argument(
        "--allow-missing-runtime",
        action="store_true",
        help="Do not fail when runtime report is missing (verification remains partial)",
    )
    args = parser.parse_args()

    try:
        mapping = load_json(args.mapping)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: cannot read mapping: {exc}")
        return 1

    styles = mapping.get("styles")
    if not isinstance(styles, list) or not styles:
        print("FAIL: mapping.styles must be non-empty list")
        return 1

    runtime: dict[str, Any] | None = None
    runtime_index: dict[str, dict[str, Any]] = {}
    registered_fonts_runtime: set[str] = set()
    if args.runtime is not None:
        try:
            runtime = load_json(args.runtime)
            runtime_index = build_runtime_index(runtime)
            runtime_fonts = runtime.get("registered_fonts", [])
            if isinstance(runtime_fonts, list):
                registered_fonts_runtime = {str(item).strip() for item in runtime_fonts if str(item).strip()}
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: cannot read runtime: {exc}")
            return 1

    plist_fonts: set[str] = set()
    if args.project_root is not None:
        plist_fonts = parse_info_plist_fonts(args.project_root)

    findings: list[str] = []
    warnings: list[str] = []

    if runtime is None and not args.allow_missing_runtime:
        findings.append("runtime report is required for strict verification")
    elif runtime is None:
        warnings.append("runtime report is missing: verification is partial")

    for style in styles:
        if not isinstance(style, dict):
            findings.append("mapping style entry is not object")
            continue

        for field in REQUIRED_STYLE_FIELDS:
            value = style.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(f"style missing required field '{field}': {style}")

        style_name = str(style.get("style_name", "")).strip()
        expected_family = str(style.get("expected_family", "")).strip()
        expected_face = str(style.get("expected_face", "")).strip()
        expected_runtime_name = str(style.get("expected_runtime_name", "")).strip()
        expected_weight = style.get("expected_weight")
        expected_style = style.get("expected_style")
        expected_file = style.get("expected_file")

        if expected_file:
            file_path = resolve_file(args.project_root, str(expected_file))
            if not file_path.exists():
                findings.append(f"[{style_name}] expected font file missing: {file_path}")

        if plist_fonts and expected_file:
            file_name = Path(str(expected_file)).name
            if file_name not in plist_fonts:
                warnings.append(
                    f"[{style_name}] expected file '{file_name}' not found in UIAppFonts entries"
                )

        runtime_entry = runtime_index.get(style_name)
        if runtime is not None and runtime_entry is None:
            findings.append(f"[{style_name}] runtime entry not found")
            continue
        if runtime_entry is None:
            continue

        if bool(runtime_entry.get("fallback_detected")):
            findings.append(f"[{style_name}] runtime fallback detected")

        runtime_name = str(runtime_entry.get("runtime_name", "")).strip()
        runtime_family = str(runtime_entry.get("runtime_family", "")).strip()
        runtime_face = str(runtime_entry.get("runtime_face", "")).strip()

        if normalize(runtime_name) != normalize(expected_runtime_name):
            findings.append(
                f"[{style_name}] runtime name mismatch: expected='{expected_runtime_name}' actual='{runtime_name}'"
            )

        if registered_fonts_runtime and expected_runtime_name not in registered_fonts_runtime:
            findings.append(f"[{style_name}] expected runtime font not in registered_fonts list")

        if normalize(runtime_family) != normalize(expected_family):
            findings.append(
                f"[{style_name}] runtime family mismatch: expected='{expected_family}' actual='{runtime_family}'"
            )
        if normalize(runtime_face) != normalize(expected_face):
            findings.append(
                f"[{style_name}] runtime face mismatch: expected='{expected_face}' actual='{runtime_face}'"
            )

        if expected_weight is not None:
            actual_weight = runtime_entry.get("runtime_weight")
            if normalize(str(actual_weight)) != normalize(str(expected_weight)):
                findings.append(
                    f"[{style_name}] weight mismatch: expected={expected_weight!r} actual={actual_weight!r}"
                )

        if expected_style is not None:
            actual_style = runtime_entry.get("runtime_style")
            if normalize(str(actual_style)) != normalize(str(expected_style)):
                findings.append(
                    f"[{style_name}] style mismatch: expected={expected_style!r} actual={actual_style!r}"
                )

    if findings:
        print(f"FAIL: {len(findings)} findings")
        for item in findings:
            print(f"- {item}")
        if warnings:
            print("WARNINGS:")
            for item in warnings:
                print(f"- {item}")
        return 1

    print("PASS: iOS font verification passed")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
