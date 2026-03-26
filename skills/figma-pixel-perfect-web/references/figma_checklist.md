# Figma Visual Fidelity Checklist (Web)

Fail condition: любой неподтвержденный critical параметр.

## 1. Scope and variant
- [ ] Подтвержден root frame и variant scope.
- [ ] Подтверждены visibility conditions.
- [ ] Подтверждены node-id всех реализуемых частей.

## 2. Layout behavior inside parent
- [ ] Edge-pin/center/stretch/fixed-size подтверждены.
- [ ] Axis ownership подтверждена.
- [ ] Intrinsic spacing отделен от accidental gap.

## 3. Typography extraction and font pipeline
- [ ] Выполнен typography inventory (including mixed styles).
- [ ] Извлечены exact family/face/style/size/line-height mode/letter-spacing mode.
- [ ] Извлечены container width, line count, baseline behavior.
- [ ] Проверены variable axes / optical size (если используются).
- [ ] Для каждого style зафиксирован source of truth.
- [ ] Для каждого style зафиксирован exact mapping style -> face -> file/source.
- [ ] Проверена легальность font source.
- [ ] Проверено реальное применение font face и отсутствие fallback.
- [ ] Проверены glyph coverage и fallback glyph substitution risk.

## 4. Compositing and micro-details
- [ ] blend/compositing/effect stack подтверждены.
- [ ] transparency inheritance и nested opacity interaction подтверждены.
- [ ] corner smoothing подтвержден.
- [ ] hairline/divider детали подтверждены.

## 5. Images, clipping, and assets
- [ ] clipping origin подтвержден.
- [ ] source of truth per asset подтвержден.
- [ ] exportability decision выполнен до кода.

## 6. Interaction geometry
- [ ] visual bounds и hit area подтверждены раздельно.

## 7. Precision and consistency
- [ ] subpixel placement подтвержден.
- [ ] repeated instances проверены.
- [ ] negative space сохранен.
- [ ] visual weight balance проверен.

## 8. Token and variant mapping
- [ ] token alias chain раскрыт до final values.
- [ ] variant property mapping перенесен структурно.
