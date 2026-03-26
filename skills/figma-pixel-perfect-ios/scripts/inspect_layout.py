#!/usr/bin/env python3
"""Strict comparator for Figma and implementation JSON specs (iOS).

Core checks:
- strict compare on critical paths
- zero numeric tolerance by default

Additional checks (partially automatable):
- repeated instance consistency
- hairline/divider detail detection
- subpixel drift detection
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_CRITICAL_PATHS = [
    "root_frame.id",
    "root_frame.width",
    "root_frame.height",
    "layout.width",
    "layout.height",
    "layout.padding.top",
    "layout.padding.trailing",
    "layout.padding.bottom",
    "layout.padding.leading",
    "layout.gap",
    "layout.constraint_behavior",
    "layout.axis_ownership",
    "typography.nature",
    "typography.font_family",
    "typography.font_face",
    "typography.font_asset_ref",
    "typography.font_file_ref",
    "typography.font_runtime_name",
    "typography.font_size",
    "typography.font_weight",
    "typography.font_style",
    "typography.line_height_mode",
    "typography.line_height",
    "typography.letter_spacing_mode",
    "typography.letter_spacing",
    "typography.baseline_alignment",
    "typography.text_container_width",
    "typography.line_count",
    "typography.glyph_coverage_confirmed",
    "typography.fallback_detected",
    "styles.colors",
    "styles.blend_mode",
    "styles.effect_stack",
    "styles.opacity.local",
    "styles.opacity.inherited",
    "styles.corner_radius",
    "styles.corner_smoothing",
    "styles.border_width",
    "styles.shadows",
    "interaction.visual_bounds",
    "interaction.hit_area_bounds",
    "assets",
    "states",
    "variants",
]

TOKEN_PATTERN = re.compile(r"([^\[\]]+)|(\[(\d+)\])")
HAIRLINE_KEYWORDS = ("hairline", "divider", "separator", "stroke", "border", "line")
NUMERIC_PATH_HINTS = ("x", "y", "width", "height", "stroke", "border", "line", "radius", "spacing", "gap")


@dataclass
class Finding:
    path: str
    expected: Any
    actual: Any
    reason: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def parse_path(path: str) -> list[Any]:
    tokens: list[Any] = []
    for match in TOKEN_PATTERN.finditer(path):
        name = match.group(1)
        index = match.group(3)
        if name is not None:
            tokens.extend(name.split("."))
        elif index is not None:
            tokens.append(int(index))
    return [tok for tok in tokens if tok != ""]


def get_by_path(data: Any, path: str) -> tuple[bool, Any]:
    current = data
    for token in parse_path(path):
        if isinstance(token, int):
            if not isinstance(current, list) or token >= len(current):
                return False, None
            current = current[token]
            continue

        if not isinstance(current, dict) or token not in current:
            return False, None
        current = current[token]
    return True, current


def read_critical_paths(figma_spec: Any, path_file: Path | None) -> list[str]:
    if path_file:
        lines = [line.strip() for line in path_file.read_text(encoding="utf-8").splitlines()]
        return [line for line in lines if line and not line.startswith("#")]

    if isinstance(figma_spec, dict) and isinstance(figma_spec.get("critical_paths"), list):
        values = [item for item in figma_spec["critical_paths"] if isinstance(item, str) and item.strip()]
        if values:
            return values

    return DEFAULT_CRITICAL_PATHS


def compare_value(expected: Any, actual: Any, tolerance: float, path: str, findings: list[Finding]) -> None:
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if math.isfinite(float(expected)) and math.isfinite(float(actual)):
            if abs(float(expected) - float(actual)) > tolerance:
                findings.append(Finding(path, expected, actual, f"numeric delta exceeds tolerance {tolerance}"))
            return

    if type(expected) is not type(actual):
        findings.append(Finding(path, expected, actual, "type mismatch"))
        return

    if isinstance(expected, dict):
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())
        for key in sorted(expected_keys - actual_keys):
            findings.append(Finding(f"{path}.{key}" if path else key, expected.get(key), None, "missing key"))
        for key in sorted(actual_keys - expected_keys):
            findings.append(Finding(f"{path}.{key}" if path else key, None, actual.get(key), "unexpected key"))
        for key in sorted(expected_keys & actual_keys):
            next_path = f"{path}.{key}" if path else key
            compare_value(expected[key], actual[key], tolerance, next_path, findings)
        return

    if isinstance(expected, list):
        if len(expected) != len(actual):
            findings.append(Finding(path, len(expected), len(actual), "list length mismatch"))
        for index, (exp_item, act_item) in enumerate(zip(expected, actual)):
            compare_value(exp_item, act_item, tolerance, f"{path}[{index}]", findings)
        return

    if expected != actual:
        findings.append(Finding(path, expected, actual, "value mismatch"))


def walk_numbers(data: Any, path: str = "") -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    if isinstance(data, dict):
        for key, value in data.items():
            next_path = f"{path}.{key}" if path else key
            out.extend(walk_numbers(value, next_path))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            next_path = f"{path}[{index}]"
            out.extend(walk_numbers(value, next_path))
    elif isinstance(data, (int, float)):
        out.append((path, float(data)))
    return out


def has_subpixel(value: float) -> bool:
    return not math.isclose(value, round(value), rel_tol=0.0, abs_tol=0.0)


def path_is_geometry(path: str) -> bool:
    lower = path.lower()
    return any(hint in lower for hint in NUMERIC_PATH_HINTS)


def check_subpixel_drift(figma_spec: Any, impl_spec: Any, tolerance: float, findings: list[Finding]) -> None:
    for path, figma_value in walk_numbers(figma_spec):
        if not path_is_geometry(path):
            continue
        if not has_subpixel(figma_value):
            continue
        exists, impl_value = get_by_path(impl_spec, path)
        if not exists or not isinstance(impl_value, (int, float)):
            continue
        if abs(figma_value - float(impl_value)) > tolerance:
            findings.append(
                Finding(path, figma_value, impl_value, "subpixel drift detected (possible rounding loss)")
            )


def collect_hairlines(spec: Any, max_width: float) -> list[tuple[str, float]]:
    result: list[tuple[str, float]] = []
    for path, value in walk_numbers(spec):
        lower = path.lower()
        if any(keyword in lower for keyword in HAIRLINE_KEYWORDS) and 0 < value <= max_width:
            result.append((path, value))
    return result


def check_hairline_coverage(figma_spec: Any, impl_spec: Any, max_width: float, findings: list[Finding], warnings: list[str]) -> None:
    figma_hairlines = collect_hairlines(figma_spec, max_width)
    impl_hairlines = collect_hairlines(impl_spec, max_width)

    if figma_hairlines and not impl_hairlines:
        findings.append(
            Finding("hairlines", len(figma_hairlines), 0, "hairline details likely lost in implementation")
        )
        return

    if figma_hairlines:
        warnings.append(
            f"Hairline candidates: figma={len(figma_hairlines)} impl={len(impl_hairlines)} (manual visual confirmation still required)"
        )


def canonical_signature(item: dict[str, Any]) -> str:
    if "signature" in item:
        payload = item["signature"]
    elif "critical_signature" in item:
        payload = item["critical_signature"]
    else:
        payload = {
            key: value
            for key, value in item.items()
            if key not in {"id", "name", "group", "instance_group", "component_key"}
        }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def check_repeated_instances(spec: Any, label: str, strict_extra: bool, findings: list[Finding], warnings: list[str]) -> None:
    if not isinstance(spec, dict) or not isinstance(spec.get("instances"), list):
        return

    groups: dict[str, list[str]] = {}
    for entry in spec["instances"]:
        if not isinstance(entry, dict):
            continue
        group = entry.get("instance_group") or entry.get("group") or entry.get("component_key")
        if not isinstance(group, str) or not group.strip():
            continue
        groups.setdefault(group, []).append(canonical_signature(entry))

    for group, signatures in groups.items():
        if len(signatures) < 2:
            continue
        unique_count = len(set(signatures))
        if unique_count > 1:
            reason = f"repeated instance group '{group}' has {unique_count} distinct signatures"
            if strict_extra:
                findings.append(Finding(f"instances.{group}", "identical signatures", f"{unique_count} variants", reason))
            else:
                warnings.append(f"[{label}] {reason} (manual confirmation required)")


def run(figma_path: Path, impl_path: Path, tolerance: float, critical_file: Path | None, max_hairline_width: float, strict_extra: bool) -> int:
    figma_spec = load_json(figma_path)
    impl_spec = load_json(impl_path)

    critical_paths = read_critical_paths(figma_spec, critical_file)
    if not critical_paths:
        print("FAIL: no critical paths provided")
        return 1

    findings: list[Finding] = []
    warnings: list[str] = []

    for critical_path in critical_paths:
        figma_exists, expected = get_by_path(figma_spec, critical_path)
        impl_exists, actual = get_by_path(impl_spec, critical_path)

        if not figma_exists:
            findings.append(Finding(critical_path, None, None, "critical path missing in figma spec"))
            continue
        if not impl_exists:
            findings.append(Finding(critical_path, expected, None, "critical path missing in implementation spec"))
            continue
        if expected is None:
            findings.append(Finding(critical_path, None, actual, "critical value is null in figma spec"))
            continue
        if actual is None:
            findings.append(Finding(critical_path, expected, None, "critical value is null in implementation spec"))
            continue

        compare_value(expected, actual, tolerance, critical_path, findings)

    check_subpixel_drift(figma_spec, impl_spec, tolerance, findings)
    check_hairline_coverage(figma_spec, impl_spec, max_hairline_width, findings, warnings)
    check_repeated_instances(figma_spec, "figma", strict_extra, findings, warnings)
    check_repeated_instances(impl_spec, "implementation", strict_extra, findings, warnings)

    if findings:
        print(f"FAIL: {len(findings)} findings")
        for item in findings:
            print(f"- {item.path}: {item.reason} | expected={item.expected!r} actual={item.actual!r}")
        if warnings:
            print("WARNINGS:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("PASS: all checks passed")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare figma_spec and impl_spec JSON with strict checks (iOS)")
    parser.add_argument("--figma", required=True, type=Path, help="Path to figma_spec JSON")
    parser.add_argument("--impl", required=True, type=Path, help="Path to implementation_spec JSON")
    parser.add_argument("--tolerance", type=float, default=0.0, help="Numeric tolerance (default: 0)")
    parser.add_argument("--critical-file", type=Path, default=None, help="Optional file with one critical path per line")
    parser.add_argument("--max-hairline-width", type=float, default=1.0, help="Maximum width to treat as hairline")
    parser.add_argument(
        "--strict-extra",
        action="store_true",
        help="Treat repeated-instance inconsistency as hard failure",
    )
    args = parser.parse_args()

    return run(
        figma_path=args.figma,
        impl_path=args.impl,
        tolerance=args.tolerance,
        critical_file=args.critical_file,
        max_hairline_width=args.max_hairline_width,
        strict_extra=args.strict_extra,
    )


if __name__ == "__main__":
    sys.exit(main())
