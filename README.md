# Figma Pixel Perfect Skills for Codex

Two production-ready Codex skills for strict Figma-to-code delivery with **Figma-first** rules and **zero approximate values**.

## Included Skills

- `figma-pixel-perfect-router`
  - First-pass router for Figma requests.
  - Always triggers on Figma URL/node-id/screen-from-design intent and routes to the strict platform skill.

- `figma-pixel-perfect-web`
  - Ultra-precise web implementation from Figma links, frames, pages, screens, components, or component sets.
  - Strong runtime typography pipeline: exact font source mapping, fallback detection, and text metrics verification.

- `figma-pixel-perfect-ios`
  - Ultra-precise iOS implementation from Figma links, frames, pages, screens, components, or component sets.
  - Strong typography pipeline: exact font discovery, registration/runtime verification, and fallback refusal.

## Why These Skills

These skills are intentionally strict for teams that need measurable fidelity, not "close enough":

- Figma is the single source of truth.
- Any visible mismatch is treated as a defect.
- Typography is the highest-priority control zone.
- Exact fonts are actively acquired and installed/registered when missing (trusted sources only).
- Missing exact font source blocks full completion.
- Runtime verification is required, not just style declaration.

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

### Option 1: copy from this repo

```bash
bash scripts/install_local.sh
```

This installs both skills into:

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

What it checks:

- required file structure
- `SKILL.md` frontmatter validity (via Codex skill validator if available)
- typography scripts CLI availability (`--help`)

## Typical Prompts That Auto-Trigger These Skills

### Web

- "Build this page from Figma"
- "Pixel perfect web from this Figma link"
- "сверстай по ссылке из Figma"

### iOS

- "Build this iOS screen from Figma"
- "собери iOS экран по Figma"

### Router

- "https://www.figma.com/design/... implement this"
- "node-id=12:34 build this screen"
- "сверстай экран по фигме"

## Typography Verification Utilities

Each skill includes practical scripts for strict typography checks:

- `scripts/verify_fonts.py`
  - verifies exact font source/face mapping
  - checks fallback signals
  - checks runtime-reported usage

- `scripts/inspect_text_metrics.py`
  - compares runtime text metrics against Figma spec
  - checks line height, line count, container width, baseline, letter spacing

## Notes

- These skills actively search, download, install/register, and apply missing exact fonts when trusted legal sources are available.
- These skills do not download fonts from untrusted sources.
- If exact legal font sources are still missing after acquisition attempts, typography is marked blocked and strict completion is not allowed.

## License

MIT
