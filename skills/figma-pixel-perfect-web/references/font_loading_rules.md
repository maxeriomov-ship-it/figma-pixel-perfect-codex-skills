# Font Loading Rules (Web)

1. Проверяй не только declarations, но и фактическую загрузку face.
2. Проверяй `document.fonts` или эквивалентные runtime данные.
3. Для критичных text nodes сверяй computed family/face/weight/style.
4. Проверяй, что computed values соответствуют mapping, а не fallback цепочке.
5. При любом fallback signal typography считается неподтвержденной.
6. Проверяй line-height/letter-spacing после рендера, а не только в CSS.
7. Проверяй container width и line count после рендера.
8. Проверяй baseline behavior, особенно для text+icon и number+label.
9. Проверяй glyph coverage для всего фактического текста.
10. Если runtime верификация невозможна, указывай blocker и не помечай typography complete.
