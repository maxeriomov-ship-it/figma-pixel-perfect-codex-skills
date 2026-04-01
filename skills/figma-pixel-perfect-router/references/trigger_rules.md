# Trigger Rules

## High-confidence Figma signals
- URL contains `figma.com/file/`
- URL contains `figma.com/design/`
- URL contains `figma.com/proto/`
- URL contains `figma.com/board/`
- text contains `node-id=`

## Intent signals (RU/EN)
- RU: `сверстай`, `собери`, `экран`, `по фигме`, `из фигмы`, `макет`
- EN: `build`, `implement`, `layout`, `screen`, `from figma`, `pixel perfect`

## Platform routing signals
- iOS signals: `ios`, `swift`, `swiftui`, `uikit`, `iphone`
- Web signals: `web`, `frontend`, `html`, `css`, `react`, `next`, `page`, `landing`

## Tie-break
- If both absent or conflicting, default route: `figma-pixel-perfect-web`.
