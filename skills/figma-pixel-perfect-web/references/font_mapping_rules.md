# Font Mapping Rules (Web)

1. Для каждого Figma text style должен существовать отдельный mapping record.
2. Mapping должен включать exact family и exact face, не только family.
3. Mapping должен указывать exact source: local file, package, existing DS mapping, platform source.
4. Mapping должен включать exact path/ref к font file или package entry.
5. Для каждого mapping нужно фиксировать expected `@font-face` declaration.
6. `@font-face` для каждого face/weight/style оформляется отдельно.
7. Нельзя сливать разные face в один record ради упрощения.
8. Нельзя использовать broad weight ranges без явного подтверждения из Figma и source.
9. Для variable fonts указывать активные axes и подтвержденные значения.
10. Если face не найден, mapping помечается blocked и typography completion запрещен.
11. Источник шрифта должен быть легальным и проверяемым.
12. Любой невалидный mapping автоматически делает typography `NOT CONFIRMED`.
