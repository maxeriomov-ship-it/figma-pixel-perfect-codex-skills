---
name: figma-pixel-perfect-ios
description: Use for ultra-precise iOS screen implementation from Figma links, frames, pages, screens, components, or component sets. Trigger on requests like "build this iOS screen from Figma", "собери iOS экран по Figma", and enforce Figma-first decisions with zero approximate values.
---

# Figma Pixel Perfect iOS

## Когда использовать
- Пользователь просит iOS экран/компонент по Figma URL, frame, page, screen, component или component set.
- Нужна сверхточная визуальная реализация без компромиссов.
- Нужен строгий typography pipeline: exact extraction -> exact font source -> exact registration -> runtime verification.

## Абсолютный приоритет
- Figma — абсолютный source of truth.
- При конфликте между точностью и удобством реализации выбирать точность.
- Типографика — зона максимального приоритета.
- Если typography подтверждена не полностью, результат не может считаться pixel perfect.

## Typography считается подтвержденной только если одновременно подтверждены и реально применены
- font family
- exact font face
- exact font file или exact platform font source
- font size
- font weight
- font style
- line height mode + exact value
- letter spacing mode + exact value
- text transform
- text alignment
- text decoration (если есть)
- paragraph spacing (если есть)
- text case
- wrapping behavior
- container width
- line count
- baseline behavior
- rendering chain без unintended fallback

## Что skill обязан делать
1. Определять root frame(s), variant scope и visibility conditions.
2. Восстанавливать точную спецификацию до начала кода.
3. Выполнять обязательный typography workflow до UI-кода.
4. Работать в существующем iOS стеке проекта: SwiftUI или UIKit по факту.
5. Использовать токены/primitives/components проекта только при полном совпадении.
6. Помечать `NOT DONE` при любом неподтвержденном critical параметре.

## Обязательный workflow
1. Определи root frame(s), variant scope, visibility conditions, node-id.
2. Восстанови точную спецификацию layout/typography/compositing/assets/states.
3. Выполни Mandatory Typography Workflow (ниже) до кода.
4. Зафиксируй feasibility risks и exportability decisions before coding.
5. Определи iOS stack проекта и реализуй строго в нем.
6. Выполни self-check по references и scripts.
7. При typography blocker или другом critical blocker выставь `NOT DONE`.

## Mandatory Typography Workflow (до кода)

### 1) Typography inventory
- Собери inventory всех text styles, text nodes, text roles в root frame.
- Раздели: повторяющиеся стили, уникальные стили, local overrides, mixed styles.
- Классифицируй: semantic text, outlined/vector text, text-as-graphic.

### 2) Exact font extraction
Для каждого text style/node извлеки:
- family, exact face/style name
- size, weight, style
- line height mode + exact value
- letter spacing mode + exact value
- paragraph spacing (если доступно)
- case, transform, decoration, alignment
- auto resize behavior, fixed/auto width
- фактический container width/height
- line count (если выводимо)
- mixed styles, kerning/font features (если доступны)
- variable font axes, optical size (если используются)
- platform-specific typography attributes (если доступны)

### 3) Font source resolution
Для каждого шрифта определить source of truth:
1. existing font files в проекте
2. existing registration setup и Info.plist entries
3. typography tokens/font helpers/design-system text primitives
4. точный platform font source
5. легальный проектный source, явно доступный в контуре проекта

### 4) Exact font mapping
Для каждого style зафиксировать mapping:
- Figma style name
- exact figma values
- expected source
- expected face
- expected file/runtime name (PostScript/runtime name, если критично)
- usage location in code
- verification status

### 5) Fallback refusal
- Нельзя молча подставлять fallback.
- Нельзя заменять custom font похожим system face.
- Нельзя подменять weight/style/italic/oblique/variable-static без подтверждения.
- При отсутствии exact source typography = `NOT CONFIRMED`.

### 6) Real usage verification (iOS)
После реализации подтвердить:
- font registration действительно выполнена
- exact face реально создается в runtime
- применяется правильный weight/style
- нет признаков fallback
- text metrics соответствуют Figma (line height/line count/container width/baseline)

## iOS-specific typography rules
- Перед любым новым подключением выполнить font discovery в проекте.
- Для custom fonts использовать точную регистрацию и точные runtime/PostScript names.
- Различать system face и custom face строго по факту.
- Не включать dynamic type/platform scaling, если это не требуется макетом или проектом.
- Для UIKit и SwiftUI нельзя подменять exact face на ближайший `.system`/`.body` style.
- Typography completion на iOS только при подтверждении source + registration + runtime usage + metrics.

## Лицензии и источники шрифтов
- Не скачивать шрифты со случайных сайтов.
- Не использовать сомнительные и нелегальные источники.
- Сначала использовать легально доступные шрифты из проекта/его инфраструктуры.
- Если exact source отсутствует, явно помечать `blocked by missing font source`.
- При таком блокере задача не может быть fully complete.

## Критичные параметры
- Root frame, variant scope, visibility conditions.
- Layout logic, per-side spacing, constraint behavior inside parent, axis ownership.
- Typography pipeline: inventory, extraction, source resolution, mapping, runtime verification.
- Реальное font usage без fallback.
- Text metrics и baseline behavior.
- Colors/fills/blend/compositing/effect order/opacity.
- Radius/corner smoothing, border/shadow/blur.
- Assets/states/variants/hit area vs visual bounds.

## Жесткие запреты
- Нельзя угадывать typography параметры.
- Нельзя считать совпадение только family достаточным.
- Нельзя игнорировать exact face/source/runtime name.
- Нельзя подменять regular/medium/semibold/bold и roman/italic/oblique.
- Нельзя игнорировать variable axes/optical size/font features, если они есть.
- Нельзя менять wrapping/container width/line count ради удобства.
- Нельзя скрывать отсутствие точного и легального font source.
- Нельзя заявлять completion при неподтвержденной typography.

## Что проверять перед завершением
- `references/figma_checklist.md`
- `references/typography_checklist.md`
- `references/layout_spacing_checklist.md`
- `references/ios_rules.md`
- `references/font_mapping_rules.md`
- `references/font_registration_rules.md`
- `references/rules_of_done.md`
- `assets/typography_mapping_template.md`
- `scripts/inspect_layout.py`
- `scripts/verify_fonts.py`
- `scripts/inspect_text_metrics.py`

## Формат финального ответа
1. Готовый код.
2. Список измененных и созданных файлов.
3. Очень короткий summary.
4. Список подтвержденных critical параметров.
5. Список переиспользованных токенов/компонентов без потери точности.
6. Список неподтвержденного/незавершенного.
7. Вывод: завершено или `NOT DONE`.
8. Отдельный Typography Block:
   - найденные text styles
   - confirmed exact fonts
   - confirmed exact faces
   - fonts, уже найденные в проекте
   - созданные mappings
   - реально зарегистрированные/примененные fonts
   - fallback risk
   - missing font source blockers
   - статус typography completion

## Если параметр не подтвержден
1. Явно отметить параметр как неподтвержденный.
2. Не выбирать ближайшее значение.
3. Не заявлять pixel perfect completion.
4. Явно фиксировать blocker и его влияние.

## Использование references, assets, scripts
- `references/font_mapping_rules.md`: строгий style->face->source mapping.
- `references/font_registration_rules.md`: правила регистрации и runtime-проверки на iOS.
- `assets/typography_mapping_template.md`: обязательная таблица mapping.
- `scripts/verify_fonts.py`: проверка registration/runtime/fallback.
- `scripts/inspect_text_metrics.py`: проверка line metrics/width/line count/baseline.

## Главный принцип
- Сначала подтвержденная точность.
- Затем переиспользование.
- Затем косметическая чистка, только если не меняет визуальный результат.
