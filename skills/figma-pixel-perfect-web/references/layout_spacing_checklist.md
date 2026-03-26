# Layout and Spacing Checklist (Web)

Fail condition: хотя бы один layout/spacing critical параметр не подтвержден.

## Container geometry
- [ ] Width/height подтверждены для контейнеров и ключевых элементов.
- [ ] Min/max ограничения подтверждены, если присутствуют.
- [ ] Subpixel значения подтверждены и не округлены автоматически.

## Constraint behavior inside parent
- [ ] Подтверждено edge-pin / center / stretch / fixed-size поведение.
- [ ] Подтверждена удерживающая логика внутри контейнера.
- [ ] Axis ownership подтверждена отдельно по X и Y.

## Spacing quality
- [ ] Padding подтвержден по каждой стороне отдельно.
- [ ] Margin подтвержден по каждой стороне отдельно.
- [ ] Gap подтвержден на каждом уровне.
- [ ] Intrinsic spacing отделен от accidental gap.

## Clipping and overflow
- [ ] Подтвержден не только факт clipping, но и clipping origin.
- [ ] Подтверждено расположение контента внутри clip области.
- [ ] Overflow behavior подтвержден.

## Thin details and separators
- [ ] Hairline/divider/separator элементы явно подтверждены.
- [ ] Тонкие stroke линии не потеряны при реализации.

## Interaction geometry
- [ ] Visual bounds и hit area подтверждены раздельно.
- [ ] Различие visual/hit bounds корректно реализовано.

## Composition
- [ ] Negative space не сжат и не перераспределен случайно.
- [ ] Visual weight balance проверен как дополнительный контроль.
