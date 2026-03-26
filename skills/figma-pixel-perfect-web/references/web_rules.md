# Web Pixel Perfect Rules

1. Figma всегда главный источник истины.
2. Типографика — зона максимального приоритета.
3. Совпадение только family name не является подтверждением.
4. Для каждого style обязателен exact face и exact source mapping.
5. Для каждого style обязателен exact loading/apply verification.
6. Fallback недопустим как тихая замена.
7. Если точный и легальный font source отсутствует, typography = blocked.
8. Variable fonts нельзя сводить к static face без подтверждения.
9. `@font-face` mappings должны быть точными по face/weight/style.
10. Text metrics и baseline behavior должны быть подтверждены после реального рендера.
11. Typography completion невозможен без runtime verification chain.
12. Любой typography blocker автоматически блокирует pixel-perfect completion.
13. Нельзя скачивать fonts из случайных или нелегальных источников.
