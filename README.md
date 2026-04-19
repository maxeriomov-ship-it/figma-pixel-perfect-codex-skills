# Codex Figma Precision Toolkit

Codex Figma Precision Toolkit provides production-ready Codex skills for teams that require high-fidelity implementation from Figma across web and iOS. The toolkit is built around strict visual accuracy, exact typography handling, and verification-first delivery rather than approximate design translation.

## Included Skills

- `figma-pixel-perfect-router`
  - First-pass router for Figma-driven requests
  - Detects Figma URLs, node IDs, and screen implementation intent, then routes to the correct strict skill
- `figma-pixel-perfect-web`
  - High-fidelity web implementation from Figma links, frames, screens, components, and component sets
  - Includes typography verification for exact font mapping, fallback detection, and text-metrics validation
- `figma-pixel-perfect-ios`
  - High-fidelity iOS implementation from Figma links, frames, screens, components, and component sets
  - Includes exact font discovery, registration checks, runtime verification, and fallback refusal

## Core Principles

- Figma remains the source of truth for layout, spacing, typography, and visual behavior
- Visible mismatches are treated as defects, not acceptable approximations
- Typography is validated at runtime, not only declared in code
- Missing exact fonts block strict completion until a trusted legal source is available
- Verification is part of delivery, not an optional cleanup step

## Repository Structure

```text
skills/
  figma-pixel-perfect-router/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/

  figma-pixel-perfect-web/
    SKILL.md
    agents/openai.yaml
    references/
    assets/
    scripts/

  figma-pixel-perfect-ios/
    SKILL.md
    agents/openai.yaml
    references/
    assets/
    scripts/

scripts/
  install_local.sh
  validate_skills.sh

examples/
  web/
  ios/
```

## Install in Codex

### Option 1: install from this repository

```bash
bash scripts/install_local.sh
```

This installs the skills into:

```text
~/.codex/skills/
```

### Option 2: manual copy

```bash
cp -R skills/figma-pixel-perfect-web ~/.codex/skills/
cp -R skills/figma-pixel-perfect-ios ~/.codex/skills/
cp -R skills/figma-pixel-perfect-router ~/.codex/skills/
```

## Validate Locally

```bash
bash scripts/validate_skills.sh
```

Validation checks:

- required file structure
- `SKILL.md` frontmatter integrity
- availability of typography CLI utilities

## Typical Prompts

### Web

- "Build this page from Figma"
- "Implement this Figma screen for web with pixel precision"
- "Сверстай экран из Figma без визуальных отклонений"

### iOS

- "Build this iOS screen from Figma"
- "Implement this Figma view for iOS with exact typography"
- "Собери экран iOS по Figma без аппроксимаций"

### Router

- "https://www.figma.com/design/... implement this"
- "node-id=12:34 build this screen"
- "Сделай этот экран по Figma"

## Typography Utilities

Each skill includes practical scripts for strict typography verification:

- `scripts/verify_fonts.py`
  - verifies exact font source and face mapping
  - detects fallback signals
  - checks runtime-reported usage
- `scripts/inspect_text_metrics.py`
  - compares runtime text metrics with the Figma specification
  - checks line height, line count, container width, baseline, and letter spacing

## Notes

- These skills can search for, install, register, and apply missing exact fonts when trusted legal sources are available
- Fonts are not downloaded from untrusted sources
- If an exact legal font source cannot be obtained, strict completion remains blocked by design

## License

MIT
