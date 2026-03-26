---
name: figma-pixel-perfect-web
description: Use for ultra-precise web implementation from Figma links, frames, pages, screens, components, or component sets. Trigger on requests like "build this page from Figma", "pixel perfect web from Figma", "сверстай по ссылке из Figma", and enforce Figma-first decisions with zero approximate values.
---

# Figma Pixel Perfect Web

## Когда использовать
- Пользователь просит web-реализацию по Figma URL, frame, screen, page, component или component set.
- Требуется сверхточное pixel perfect соответствие без approximate values.
- Задача включает строгий typography pipeline: от извлечения параметров до runtime-подтверждения фактического face.

## Абсолютный приоритет
- Figma — главный и абсолютный source of truth.
- При конфликте между точностью и удобством реализации всегда выбирать точность.
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
1. Определять root frame(s), variant scope, visibility conditions.
2. Полностью восстанавливать спецификацию до начала кода.
3. Выполнять обязательный typography workflow до UI-кода.
4. Работать строго в существующем web стеке проекта.
5. Использовать существующие токены/компоненты только при полном визуальном и метрик-совпадении.
6. Помечать задачу `NOT DONE`, если любой critical параметр не подтвержден, особенно typography.

## Обязательный workflow
1. Определи root frame(s), variant scope, visibility conditions и node-id.
2. Восстанови точную спецификацию layout/typography/style/states/assets.
3. Выполни обязательный Typography Workflow (ниже) до кода.
4. Зафиксируй feasibility risks и exportability decisions before coding.
5. Проверь source-of-truth для каждого asset (иконки/изображения/сложный декор).
6. Реализуй код только по подтвержденным значениям из Figma.
7. Выполни self-check по reference-файлам и scripts.
8. Если есть typography blocker или иной critical blocker, статус только `NOT DONE`.

## Mandatory Typography Workflow (до кода)

### 1) Typography inventory
- Собери inventory всех text styles, text nodes и text roles в root frame.
- Раздели: повторяющиеся стили, уникальные стили, локальные overrides, mixed styles.
- Отдельно классифицируй: semantic text, outlined/vector text, text-as-graphic.

### 2) Exact font extraction
Для каждого text style/node извлеки:
- family, exact face/style name
- size, weight, style
- line height mode + exact value
- letter spacing mode + exact value
- paragraph spacing (если доступно)
- case, transform, decoration, alignment
- auto-resize behavior, fixed/auto width
- фактический container width/height
- line count (если выводимо)
- mixed styles внутри строк
- kerning/font features (если доступны)
- variable font axes и optical size (если используются)
- platform-specific typography attributes (если доступны)

### 3) Font source resolution
Для каждого нужного шрифта определи source of truth в таком порядке:
1. existing local font files в проекте
2. existing `@font-face` declarations
3. typography/design tokens и design-system mappings
4. package-based font setup
5. легальный проектный источник, явно доступный в контуре проекта

### 4) Exact font mapping
Для каждого style создай mapping:
- Figma style name
- exact figma typography values
- expected font source
- expected face
- expected file/source ref
- code usage location
- verification status

### 5) Fallback refusal
- Нельзя молча подставлять fallback.
- Нельзя заменять custom font похожим системным.
- Нельзя подменять weight/style/italic/oblique/variable-static без подтверждения.
- Если exact source отсутствует: typography = `NOT CONFIRMED`.

### 6) Real usage verification (Web)
После реализации обязательно подтвердить:
- font реально загрузился (а не только объявлен)
- `@font-face` mapping соответствует exact face/weight/style
- computed style у целевых элементов соответствует expected face
- признаков browser fallback нет
- text metrics совпадают с Figma: line height, line count, width, letter spacing, baseline behavior
- glyph coverage достаточна, скрытой glyph substitution нет

## Web-specific typography rules
- Перед любым новым подключением выполняй font discovery внутри проекта.
- Для локальных шрифтов используй отдельный точный `@font-face` на каждый face/weight/style.
- Не объединяй разные начертания в один mapping без подтверждения.
- Если используется variable font: оси применяй только при подтверждении из Figma; иначе typography не завершена.
- Признаки browser fallback автоматически делают typography неподтвержденной.

## Лицензии и источники шрифтов
- Не скачивать шрифты со случайных сайтов.
- Не использовать сомнительные или нелегальные источники.
- Сначала использовать то, что уже есть в проекте или легально доступно в проекте.
- Если exact и легальный source отсутствует, явно помечать `blocked by missing font source`.
- При таком блокере задача может быть частично реализована, но не fully complete.

## Критичные параметры
- Root frame(s), variant scope, visibility conditions.
- Layout logic, per-side spacing, constraint behavior inside parent, axis ownership.
- Typography pipeline: inventory, extraction, source resolution, mapping, runtime verification.
- Реальное font usage без fallback.
- Text metrics и baseline behavior.
- Colors/fills/blend/compositing/effect order/opacity.
- Radius/corner smoothing, border/shadow/blur.
- Assets/states/variants/hit area vs visual bounds.

## Жесткие запреты
- Нельзя угадывать и подставлять приблизительные typography values.
- Нельзя считать совпадение только family name достаточным.
- Нельзя игнорировать exact face.
- Нельзя подменять regular/medium/semibold/bold или roman/italic/oblique.
- Нельзя игнорировать variable axes/optical size/font features при их наличии.
- Нельзя менять wrapping, container width, line count ради удобства реализации.
- Нельзя скрывать отсутствие точного и легального font source.
- Нельзя заявлять completion при неподтвержденной typography.

## Что проверять перед завершением
- `references/figma_checklist.md`
- `references/typography_checklist.md`
- `references/layout_spacing_checklist.md`
- `references/web_rules.md`
- `references/font_mapping_rules.md`
- `references/font_loading_rules.md`
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
   - реально загруженные fonts
   - fallback risk
   - missing font source blockers
   - статус typography completion

## Если параметр не подтвержден
1. Явно отметить параметр как неподтвержденный.
2. Не выбирать ближайшее значение.
3. Не заявлять pixel perfect completion.
4. Явно фиксировать блокеры и их влияние.

## Использование references, assets, scripts
- `references/font_mapping_rules.md`: строгие правила style->face->source mapping.
- `references/font_loading_rules.md`: web-runtime проверка загрузки/применения/fallback.
- `assets/typography_mapping_template.md`: обязательная таблица для фиксации mapping.
- `scripts/verify_fonts.py`: проверка источников, face availability, fallback signals.
- `scripts/inspect_text_metrics.py`: проверка width/line-height/line-count/letter-spacing/baseline.

## Главный принцип
- Сначала подтвержденная точность.
- Затем переиспользование.
- Затем косметическая чистка кода, только если она не меняет визуальный результат.
