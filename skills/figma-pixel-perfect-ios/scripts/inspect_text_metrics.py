#!/usr/bin/env python3
"""Strict text metrics comparator for iOS typography verification.

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


def as_float(value: Any) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"non-numeric value: {value!r}")
    return float(value)


def compare_values(expected: dict[str, Any], actual: dict[str, Any], tolerance: float) -> list[str]:
    findings: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in expected:
            findings.append(f"missing figma field '{field}'")
        if field not in actual:
            findings.append(f"missing runtime field '{field}'")

    for numeric_field in ("container_width", "line_height", "letter_spacing"):
        try:
            e = as_float(expected.get(numeric_field))
            a = as_float(actual.get(numeric_field))
        except ValueError as exc:
            findings.append(f"{numeric_field}: {exc}")
            continue
        if abs(e - a) > tolerance:
            findings.append(
                f"{numeric_field} mismatch: expected={e} actual={a} tolerance={tolerance}"
            )

    if expected.get("line_count") != actual.get("line_count"):
        findings.append(
            f"line_count mismatch: expected={expected.get('line_count')!r} actual={actual.get('line_count')!r}"
        )

    exp_baseline = expected.get("baseline")
    run_baseline = actual.get("baseline")
    if exp_baseline is not None or run_baseline is not None:
        if exp_baseline is None or run_baseline is None:
            findings.append(f"baseline incomplete: figma={exp_baseline!r} runtime={run_baseline!r}")
        else:
            if abs(as_float(exp_baseline) - as_float(run_baseline)) > tolerance:
                findings.append(
                    f"baseline mismatch: expected={exp_baseline!r} actual={run_baseline!r}"
                )

    if bool(actual.get("fallback_detected")):
        findings.append("fallback_detected=true")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare iOS text metrics against Figma")
    parser.add_argument("--figma", required=True, type=Path, help="Figma text metrics JSON")
    parser.add_argument("--runtime", required=True, type=Path, help="Runtime text metrics JSON")
    parser.add_argument("--tolerance", type=float, default=0.0, help="Numeric tolerance (default: 0)")
    args = parser.parse_args()

    try:
        figma = load_json(args.figma)
        runtime = load_json(args.runtime)
        figma_index = to_index(figma)
        runtime_index = to_index(runtime)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}")
        return 1

    findings: list[str] = []
    warnings: list[str] = []

    for style_name, expected in figma_index.items():
        actual = runtime_index.get(style_name)
        if actual is None:
            findings.append(f"[{style_name}] runtime metrics entry missing")
            continue
        style_findings = compare_values(expected, actual, args.tolerance)
        findings.extend([f"[{style_name}] {item}" for item in style_findings])

    extra_runtime = sorted(set(runtime_index) - set(figma_index))
    for style_name in extra_runtime:
        warnings.append(f"[{style_name}] runtime style has no figma counterpart")

    if findings:
        print(f"FAIL: {len(findings)} findings")
        for item in findings:
            print(f"- {item}")
        if warnings:
            print("WARNINGS:")
            for item in warnings:
                print(f"- {item}")
        return 1

    print("PASS: text metrics aligned")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
