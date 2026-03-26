#!/usr/bin/env python3
"""Verify web font mapping, source availability, and fallback signals.

Expected mapping JSON shape:
{
  "styles": [
    {
      "style_name": "Heading/H1",
      "expected_family": "Inter",
      "expected_face": "Inter SemiBold",
      "expected_source": "project-local",
      "expected_file": "assets/fonts/Inter-SemiBold.woff2",
      "expected_weight": 600,
      "expected_style": "normal"
    }
  ]
}

Runtime JSON (optional):
{
  "fonts_status": "loaded",
  "entries": [
    {
      "style_name": "Heading/H1",
      "computed_family": "Inter",
      "computed_face": "Inter SemiBold",
      "computed_weight": 600,
      "computed_style": "normal",
      "fallback_detected": false
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_STYLE_FIELDS = (
    "style_name",
    "expected_family",
    "expected_face",
    "expected_source",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def iter_css_files(project_root: Path) -> list[Path]:
    patterns = ("*.css", "*.scss", "*.sass", "*.less", "*.styl")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(project_root.rglob(pattern))
    return files


def search_font_face(css_files: list[Path], expected_face: str) -> bool:
    face_norm = normalize(expected_face)
    for css in css_files:
        try:
            text = css.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "@font-face" not in text:
            continue
        if face_norm in normalize(text):
            return True
    return False


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
    out: dict[str, dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, dict):
            continue
        name = item.get("style_name")
        if isinstance(name, str) and name.strip():
            out[name] = item
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify exact web font mapping and runtime usage")
    parser.add_argument("--mapping", required=True, type=Path, help="Typography mapping JSON")
    parser.add_argument("--project-root", type=Path, default=None, help="Project root for file/discovery checks")
    parser.add_argument("--runtime", type=Path, default=None, help="Runtime font report JSON")
    parser.add_argument(
        "--allow-missing-runtime",
        action="store_true",
        help="Do not fail if runtime report is missing (still warns and keeps verification partial)",
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
    if args.runtime is not None:
        try:
            runtime = load_json(args.runtime)
            runtime_index = build_runtime_index(runtime)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: cannot read runtime: {exc}")
            return 1

    css_files: list[Path] = []
    if args.project_root is not None:
        css_files = iter_css_files(args.project_root)

    findings: list[str] = []
    warnings: list[str] = []

    if runtime is None and not args.allow_missing_runtime:
        findings.append("runtime report is required for strict verification")
    elif runtime is None:
        warnings.append("runtime report is missing: verification is partial")

    if runtime is not None:
        fonts_status = runtime.get("fonts_status")
        if isinstance(fonts_status, str) and normalize(fonts_status) not in {"loaded", "ready", "complete"}:
            findings.append(f"runtime fonts_status is not loaded: {fonts_status}")

    for style in styles:
        if not isinstance(style, dict):
            findings.append("mapping style entry is not object")
            continue

        for field in REQUIRED_STYLE_FIELDS:
            value = style.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(f"style missing required field '{field}': {style}")

        style_name = str(style.get("style_name", "")).strip()
        expected_face = str(style.get("expected_face", "")).strip()
        expected_family = str(style.get("expected_family", "")).strip()
        expected_weight = style.get("expected_weight")
        expected_style = style.get("expected_style")
        expected_file = style.get("expected_file")

        if expected_file:
            file_path = resolve_file(args.project_root, str(expected_file))
            if not file_path.exists():
                findings.append(f"[{style_name}] expected font file missing: {file_path}")

        if css_files and expected_face and not search_font_face(css_files, expected_face):
            warnings.append(f"[{style_name}] no @font-face mention found for face '{expected_face}'")

        runtime_entry = runtime_index.get(style_name)
        if runtime is not None and runtime_entry is None:
            findings.append(f"[{style_name}] runtime entry not found")
            continue
        if runtime_entry is None:
            continue

        if bool(runtime_entry.get("fallback_detected")):
            findings.append(f"[{style_name}] runtime fallback detected")

        computed_family = str(runtime_entry.get("computed_family", "")).strip()
        computed_face = str(runtime_entry.get("computed_face", "")).strip()

        if normalize(expected_family) and normalize(computed_family) != normalize(expected_family):
            findings.append(
                f"[{style_name}] computed_family mismatch: expected='{expected_family}' actual='{computed_family}'"
            )
        if normalize(expected_face) and normalize(computed_face) != normalize(expected_face):
            findings.append(
                f"[{style_name}] computed_face mismatch: expected='{expected_face}' actual='{computed_face}'"
            )

        if expected_weight is not None:
            actual_weight = runtime_entry.get("computed_weight")
            if actual_weight != expected_weight:
                findings.append(
                    f"[{style_name}] weight mismatch: expected={expected_weight!r} actual={actual_weight!r}"
                )

        if expected_style is not None:
            actual_style = runtime_entry.get("computed_style")
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

    print("PASS: font verification passed")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
