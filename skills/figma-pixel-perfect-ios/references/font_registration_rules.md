# Font Registration Rules (iOS)

1. Перед регистрацией проверить, что нужный font уже не подключен в проекте.
2. Для custom fonts фиксировать точные file names и runtime/PostScript names.
3. Проверять фактическую регистрацию (Info.plist, bundle inclusion, runtime availability).
4. Нельзя считать регистрацию завершенной без runtime-подтверждения доступности face.
5. Нельзя подменять отсутствующий custom face на `.system` или близкий face.
6. Нельзя считать UIFont/Font корректным без подтверждения exact runtime name.
7. Dynamic Type не включать, если это не требуется макетом или проектными требованиями.
8. Проверять, что фактически применен нужный face/weight/style в коде.
9. При fallback signal typography помечается неподтвержденной.
10. Если exact face отсутствует локально, обязателен auto-search + auto-download + auto-register из trusted source.
11. После registration обязателен runtime-check доступности exact runtime/PostScript name.
12. Если exact и легальный source отсутствует после обязательной попытки acquisition, фиксировать blocker и не закрывать typography.
