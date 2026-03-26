# Typography Checklist (iOS)

Fail condition: хотя бы один typography параметр не подтвержден.

## A. Typography inventory
- [ ] Все text nodes и text roles в root frame инвентаризированы.
- [ ] Повторяющиеся styles сгруппированы.
- [ ] Уникальные styles выделены.
- [ ] Local overrides отмечены.
- [ ] Mixed styles внутри text blocks отмечены.
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
- [ ] variable axes / optical size / font features подтверждены, если используются.

## C. Font source and registration mapping
- [ ] Для каждого style определен exact source of truth.
- [ ] Для каждого style определен exact face.
- [ ] Для каждого style определен exact file/runtime/PostScript name.
- [ ] Mapping style -> source -> runtime face -> usage location зафиксирован.
- [ ] Проверена легальность font source.
- [ ] При отсутствии exact source поставлен blocker.

## D. Runtime usage verification (iOS)
- [ ] Нужные fonts зарегистрированы.
- [ ] Нужные faces реально доступны в runtime.
- [ ] Применяется expected face, а не ближайший fallback.
- [ ] Применяется expected weight/style.
- [ ] Нет fallback substitution.

## E. Text metrics verification
- [ ] line-height после рендера совпадает.
- [ ] line count совпадает.
- [ ] text container width совпадает.
- [ ] letter spacing после рендера совпадает.
- [ ] baseline behavior совпадает.
- [ ] wrapping совпадает фактически.

## F. Glyph coverage and fallback risk
- [ ] glyph coverage достаточна для текста макета.
- [ ] нет скрытой подмены glyphs fallback-шрифтами.
- [ ] fallback risk явно отмечен или устранен.

## G. Completion blockers
- [ ] если отсутствует exact и легальный font source, typography помечена как blocked.
- [ ] typography не отмечена complete при неподтвержденных source/face/registration/runtime/metrics.
