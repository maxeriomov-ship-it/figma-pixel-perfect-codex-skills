#!/usr/bin/env python3
"""Strict text metrics comparator for web typography verification.

Expected JSON shape for both --figma and --runtime:
{
  "entries": [
    {
      "style_name": "Heading/H1",
      "container_width": 320,
      "line_height": 28,
      "line_count": 2,
      "letter_spacing": 0,
      "baseline": 22.5,
      "fallback_detected": false
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "style_name",
    "container_width",
    "line_height",
    "line_count",
    "letter_spacing",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def to_index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("entries must be a list")
    out: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("entry must be object")
        style_name = entry.get("style_name")
        if not isinstance(style_name, str) or not style_name.strip():
            raise ValueError(f"invalid style_name in entry: {entry}")
        out[style_name] = entry
    return out


def numeric_close(expected: Any, actual: Any, tolerance: float) -> bool:
    if not isinstance(expected, (int, float)) or not isinstance(actual, (int, float)):
        return False
    return abs(float(expected) - float(actual)) <= tolerance


def compare(figma: dict[str, Any], runtime: dict[str, Any], tolerance: float) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    warnings: list[str] = []

    figma_index = to_index(figma)
    runtime_index = to_index(runtime)

    for style_name, figma_entry in figma_index.items():
        runtime_entry = runtime_index.get(style_name)
        if runtime_entry is None:
            findings.append(f"[{style_name}] runtime metrics entry missing")
            continue

        if bool(runtime_entry.get("fallback_detected")):
            findings.append(f"[{style_name}] fallback_detected=true")

        for field in REQUIRED_FIELDS:
            if field not in figma_entry:
                findings.append(f"[{style_name}] figma missing field '{field}'")
            if field not in runtime_entry:
                findings.append(f"[{style_name}] runtime missing field '{field}'")

        for field in ("container_width", "line_height", "letter_spacing"):
            expected = figma_entry.get(field)
            actual = runtime_entry.get(field)
            if not numeric_close(expected, actual, tolerance):
                findings.append(
                    f"[{style_name}] {field} mismatch: expected={expected!r} actual={actual!r} tol={tolerance}"
                )

        expected_lines = figma_entry.get("line_count")
        actual_lines = runtime_entry.get("line_count")
        if expected_lines != actual_lines:
            findings.append(
                f"[{style_name}] line_count mismatch: expected={expected_lines!r} actual={actual_lines!r}"
            )

        figma_baseline = figma_entry.get("baseline")
        runtime_baseline = runtime_entry.get("baseline")
        if figma_baseline is not None or runtime_baseline is not None:
            if figma_baseline is None or runtime_baseline is None:
                findings.append(
                    f"[{style_name}] baseline incomplete: figma={figma_baseline!r} runtime={runtime_baseline!r}"
                )
            elif not numeric_close(figma_baseline, runtime_baseline, tolerance):
                findings.append(
                    f"[{style_name}] baseline mismatch: expected={figma_baseline!r} actual={runtime_baseline!r}"
                )

        if not math.isfinite(float(runtime_entry.get("container_width", 0))):
            warnings.append(f"[{style_name}] runtime container_width is non-finite")

    extra_runtime = sorted(set(runtime_index) - set(figma_index))
    for style_name in extra_runtime:
        warnings.append(f"[{style_name}] runtime style has no figma counterpart")

    return findings, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare web text metrics against Figma")
    parser.add_argument("--figma", required=True, type=Path, help="Figma text metrics JSON")
    parser.add_argument("--runtime", required=True, type=Path, help="Runtime text metrics JSON")
    parser.add_argument("--tolerance", type=float, default=0.0, help="Numeric tolerance (default: 0)")
    args = parser.parse_args()

    try:
        figma = load_json(args.figma)
        runtime = load_json(args.runtime)
        findings, warnings = compare(figma, runtime, args.tolerance)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}")
        return 1

    if findings:
        print(f"FAIL: {len(findings)} findings")
        for finding in findings:
            print(f"- {finding}")
        if warnings:
            print("WARNINGS:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("PASS: text metrics aligned")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
