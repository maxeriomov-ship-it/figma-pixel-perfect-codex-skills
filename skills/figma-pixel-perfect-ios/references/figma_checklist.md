# Figma Visual Fidelity Checklist (iOS)

Fail condition: любой неподтвержденный critical параметр.

## 1. Scope and visibility
- [ ] Подтвержден root frame(s) и точный variant scope.
- [ ] Подтверждены visibility conditions (видимые/скрытые/чужие state слои).
- [ ] Подтверждены node-id всех реализуемых частей.

## 2. Constraint behavior inside parent
- [ ] Подтверждено pin/center/stretch/fixed-size поведение элемента внутри parent.
- [ ] Подтверждена логика удержания в контейнере.
- [ ] Подтверждена axis ownership по X/Y.
- [ ] Intrinsic spacing отделен от accidental gap.

## 3. Typography extraction and font pipeline
- [ ] Выполнен typography inventory (including mixed styles).
- [ ] Извлечены exact family/face/style/size/line-height mode/letter-spacing mode.
- [ ] Извлечены container width, line count, baseline behavior.
- [ ] Проверены variable axes / optical size (если используются).
- [ ] Для каждого style зафиксирован source of truth.
- [ ] Для каждого style зафиксирован mapping style -> face -> source/runtime name.
- [ ] Проверена легальность font source.
- [ ] Проверено реальное применение font face и отсутствие fallback.
- [ ] Проверены glyph coverage и fallback glyph substitution risk.

## 4. Compositing and effects
- [ ] Подтвержден blend mode/compositing.
- [ ] Подтвержден effect stacking order.
- [ ] Подтверждена transparency inheritance.
- [ ] Подтверждено nested opacity/fill interaction.
- [ ] Подтвержден corner smoothing (если есть).

## 5. Fine details
- [ ] Подтверждены hidden dividers/hairline details.
- [ ] Подтверждены тонкие separators/strokes.

## 6. Images and clipping
- [ ] Подтвержден real clipping origin.
- [ ] Подтверждено положение контента внутри clip области.
- [ ] Подтверждены crop/fit/fill/aspect/masks/overlays.
- [ ] Для каждого asset определен source of truth.
- [ ] Выполнен exportability decision before coding для сложных элементов.

## 7. Interaction geometry
- [ ] Подтверждены visual bounds интерактивных элементов.
- [ ] Подтверждены hit area bounds.
- [ ] Если bounds различаются, различие реализовано намеренно и точно.

## 8. Precision and consistency
- [ ] Подтвержден subpixel placement там, где он есть.
- [ ] Подтверждена consistency across repeated instances.
- [ ] Negative space сохранен.
- [ ] Visual weight balance проверен как дополнительный контроль.

## 9. Tokens and variants
- [ ] Token alias chain раскрыт до конечных значений.
- [ ] Variant property mapping перенесен структурно.
- [ ] Риск-зоны неточного переноса помечены до кода.
