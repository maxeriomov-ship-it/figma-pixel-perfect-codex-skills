# Rules of Done (Web)

Задача считается завершенной только если выполнены все условия:

- [ ] Root frame(s), variant scope и visibility conditions подтверждены.
- [ ] Все critical параметры подтверждены.
- [ ] Constraint behavior, axis ownership, spacing logic подтверждены.
- [ ] Compositing/effect order/hairline/subpixel проверки пройдены.
- [ ] Asset source-of-truth и exportability decisions подтверждены.

Typography cannot be marked complete unless:
- [ ] all critical text styles are inventoried
- [ ] all exact font sources are confirmed
- [ ] all exact faces are confirmed
- [ ] all required fonts are legally available
- [ ] all required fonts are properly loaded
- [ ] real runtime usage is verified
- [ ] no critical fallback is detected
- [ ] glyph coverage is sufficient for the design text
- [ ] text metrics align with Figma for strict pixel-perfect criteria

Дополнительно:
- [ ] если exact font source отсутствует, задача может быть частично реализована, но не может быть marked fully complete по строгим критериям.

Если хотя бы один пункт не выполнен:
- Статус: `NOT DONE`.
