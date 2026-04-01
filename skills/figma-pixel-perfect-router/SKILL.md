---
name: figma-pixel-perfect-router
description: Always trigger on any Figma URL, node-id, or request to build/implement/layout a screen from Figma. Routes explicitly to $figma-pixel-perfect-web or $figma-pixel-perfect-ios and rejects non-routed execution for Figma tasks.
---

# Figma Pixel Perfect Router

## When To Use
- Any input contains a Figma URL.
- Any input contains `node-id` or mentions frame/page/component in Figma context.
- Any request asks to build/implement/layout/code a screen from a design.

## Mandatory Routing Rule
- If a Figma signal is detected, this router must activate.
- Router must explicitly invoke exactly one target skill:
  - `$figma-pixel-perfect-web` for web/frontend/html/css/react/next requests.
  - `$figma-pixel-perfect-ios` for iOS/swift/swiftui/uikit requests.
- If platform is ambiguous, default route is `$figma-pixel-perfect-web` and mark platform assumption explicitly.

## Invalid State
- For a Figma request, proceeding without web/iOS pixel-perfect skill invocation is invalid.
- If target skill was not invoked, response must be treated as incomplete and rerouted.

## Deterministic Trigger Hints
- Detect URL patterns: `figma.com/file/`, `figma.com/design/`, `figma.com/proto/`, `figma.com/board/`, `node-id=`.
- Detect RU/EN verbs: `сверстай`, `собери экран`, `верстка`, `build`, `implement`, `pixel perfect`, `from figma`.

## Output Contract
For routed tasks, final answer must include `Skill Invocation Audit`:
- `router_skill_name: figma-pixel-perfect-router`
- `router_trigger_reason`
- `target_skill_name`
- `target_selection_reason`
- `platform_assumption` (if any)

## Quick Check
Use `scripts/smoke_router.py` to validate detection/routing on sample prompts.
