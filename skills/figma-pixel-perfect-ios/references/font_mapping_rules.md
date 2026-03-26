# Font Mapping Rules (iOS)

1. Для каждого Figma text style нужен отдельный mapping record.
2. Mapping должен включать exact family + exact face, не только family.
3. Mapping обязан содержать expected runtime/PostScript name, если используется custom font.
4. Mapping обязан фиксировать exact source: local file, package, existing token primitive, platform source.
5. Mapping обязан фиксировать usage location в SwiftUI/UIKit коде.
6. Нельзя объединять разные face в один mapping.
7. Нельзя подменять italic/oblique на normal.
8. Нельзя подменять semibold/bold/medium на ближайший вес.
9. Для variable fonts фиксировать axes и их confirmed values.
10. Если face/source не подтвержден, mapping получает blocked status.
11. Любой blocked mapping запрещает typography completion.
12. Источник шрифта должен быть легальным и проверяемым.
