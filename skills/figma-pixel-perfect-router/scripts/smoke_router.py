#!/usr/bin/env python3
"""Smoke test for Figma router skill trigger and target routing."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

FIGMA_PATTERNS = [
    r"figma\.com/file/",
    r"figma\.com/design/",
    r"figma\.com/proto/",
    r"figma\.com/board/",
    r"node-id=",
]

INTENT_PATTERNS = [
    r"\bbuild\b",
    r"\bimplement\b",
    r"\blayout\b",
    r"\bscreen\b",
    r"pixel\s*perfect",
    r"from\s+figma",
    r"сверст",
    r"собери",
    r"экран",
    r"по\s+figma",
    r"из\s+figma",
]

IOS_PATTERNS = [r"\bios\b", r"swiftui", r"\bswift\b", r"uikit", r"iphone"]
WEB_PATTERNS = [r"\bweb\b", r"frontend", r"html", r"css", r"react", r"next", r"landing", r"page"]


@dataclass
class Result:
    trigger: bool
    target: str | None


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def route(prompt: str) -> Result:
    text = prompt.strip()
    figma = has_any(text, FIGMA_PATTERNS)
    intent = has_any(text, INTENT_PATTERNS)

    if not (figma or (intent and "figma" in text.lower())):
        return Result(False, None)

    ios = has_any(text, IOS_PATTERNS)
    web = has_any(text, WEB_PATTERNS)

    if ios and not web:
        return Result(True, "figma-pixel-perfect-ios")
    return Result(True, "figma-pixel-perfect-web")


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test router trigger/routing")
    parser.add_argument("--cases", type=Path, required=True, help="JSON with test cases")
    args = parser.parse_args()

    data = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        print("FAIL: cases must be non-empty list")
        return 1

    failures = []
    for idx, case in enumerate(cases, start=1):
        prompt = case.get("prompt", "")
        expected_trigger = bool(case.get("expect_trigger", False))
        expected_target = case.get("expect_target")

        got = route(prompt)
        if got.trigger != expected_trigger:
            failures.append(f"#{idx} trigger mismatch: expected={expected_trigger} got={got.trigger}")
            continue
        if expected_trigger and expected_target != got.target:
            failures.append(f"#{idx} target mismatch: expected={expected_target} got={got.target}")

    if failures:
        print(f"FAIL: {len(failures)} routing mismatches")
        for f in failures:
            print(f"- {f}")
        return 1

    print(f"PASS: {len(cases)} cases matched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
