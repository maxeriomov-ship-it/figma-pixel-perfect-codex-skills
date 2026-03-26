# Typography Checklist (Web)

Fail condition: любой неподтвержденный typography пункт.

## A. Typography inventory
- [ ] Все text nodes и text roles в root frame инвентаризированы.
- [ ] Повторяющиеся styles сгруппированы.
- [ ] Уникальные styles выделены.
- [ ] Local override случаи отмечены.
- [ ] Mixed styles внутри text blocks отмечены и не потеряны.
- [ ] Text nature классифицирован: semantic / outlined / graphic.

## B. Exact extraction from Figma
- [ ] family подтвержден.
- [ ] exact face/style name подтвержден.
- [ ] size/weight/style подтверждены.
- [ ] line height mode + value подтверждены.
- [ ] letter spacing mode + value подтверждены.
- [ ] paragraph spacing подтвержден (если есть).
- [ ] text case / transform / decoration подтверждены.
- [ ] alignment подтвержден.
- [ ] auto-resize behavior текста подтвержден.
- [ ] text container width/height подтверждены.
- [ ] line count подтвержден.
- [ ] baseline behavior подтвержден.
- [ ] kerning/font features подтверждены, если используются.
- [ ] variable axes / optical size подтверждены, если используются.

## C. Font source mapping
- [ ] Для каждого style определен exact source of truth.
- [ ] Для каждого style определен exact face.
- [ ] Для каждого style определен exact file/runtime source.
- [ ] Mapping style -> source -> usage location зафиксирован.
- [ ] Проверена легальность источника.
- [ ] При отсутствии exact source выставлен blocker, без скрытых fallback.

## D. Loading and runtime usage verification (Web)
- [ ] Font действительно загружается (не только объявлен).
- [ ] `@font-face` mapping корректен по face/weight/style.
- [ ] Computed family совпадает с expected.
- [ ] Computed face совпадает с expected.
- [ ] Computed weight/style совпадают с expected.
- [ ] Browser fallback signals отсутствуют.

## E. Text metrics verification
- [ ] line-height после рендера совпадает.
- [ ] line count совпадает.
- [ ] text container width совпадает.
- [ ] letter spacing после рендера совпадает.
- [ ] baseline behavior совпадает.
- [ ] wrapping совпадает фактически, а не только декларативно.

## F. Glyph coverage and fallback risk
- [ ] glyph coverage достаточна для всего текста.
- [ ] нет скрытой подмены glyphs fallback-шрифтами.
- [ ] fallback risk явно отмечен или устранен.

## G. Completion blockers
- [ ] если отсутствует exact и легальный font source, typography помечена как blocked.
- [ ] typography не отмечена complete при неподтвержденных source/face/loading/metrics.
