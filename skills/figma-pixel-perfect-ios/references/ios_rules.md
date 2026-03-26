# iOS Pixel Perfect Rules

1. Figma всегда абсолютный source of truth.
2. Типографика — максимальный приоритет контроля.
3. Совпадение только family name не является подтверждением.
4. Для каждого style обязателен exact face и exact source mapping.
5. Для каждого style обязателен exact registration/runtime verification.
6. Fallback недопустим как тихая замена.
7. Если точный и легальный font source отсутствует, typography = blocked.
8. Variable fonts нельзя сводить к static face без подтверждения.
9. Нельзя подменять custom face на system face из-за визуального сходства.
10. Не включать dynamic type scaling, если это не требуется макетом/проектом.
11. UIKit/SwiftUI не должны использовать ближайший стандартный text style вместо exact face.
12. Text metrics и baseline behavior должны подтверждаться после runtime рендера.
13. Любой typography blocker автоматически блокирует pixel-perfect completion.
