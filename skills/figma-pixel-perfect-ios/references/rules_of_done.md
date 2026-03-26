# Rules of Done (iOS)

Задача считается завершенной только если выполнены все условия:

- [ ] Root frame(s), variant scope и visibility conditions подтверждены.
- [ ] Все critical параметры подтверждены численно/структурно.
- [ ] Constraint behavior inside parent и axis ownership подтверждены.
- [ ] Semantic text vs vector/graphic text классификация подтверждена.
- [ ] Blend/compositing/effect order/opacity inheritance подтверждены.
- [ ] Baseline alignment подтвержден.
- [ ] Hairline/separator микро-детали подтверждены.
- [ ] Per-side spacing подтвержден по каждой стороне.
- [ ] Clipping origin подтвержден.
- [ ] Hit area и visual bounds подтверждены раздельно.
- [ ] Token alias chains раскрыты до конечных значений.
- [ ] Source of truth per asset зафиксирован.
- [ ] Exportability decision выполнен до кодирования сложных элементов.
- [ ] Feasibility risks отмечены и покрыты проверками.
- [ ] Repeated instances проверены на реальную идентичность/различие.
- [ ] Subpixel/negative-space/visual-weight проверки выполнены.
- [ ] Все checklist и script проверки пройдены.

Typography cannot be marked complete unless:
- [ ] all critical text styles are inventoried
- [ ] all exact font sources are confirmed
- [ ] all exact faces are confirmed
- [ ] all required fonts are legally available
- [ ] all required fonts are properly registered
- [ ] real runtime usage is verified
- [ ] no critical fallback is detected
- [ ] glyph coverage is sufficient for design text
- [ ] text metrics align with Figma for strict pixel-perfect criteria

Дополнительно:
- [ ] если exact font source отсутствует, задача может быть частично реализована, но не может быть marked fully complete по строгим критериям.

Если хотя бы один пункт не выполнен:
- Статус: `NOT DONE`.
- Pixel perfect completion заявлять запрещено.
