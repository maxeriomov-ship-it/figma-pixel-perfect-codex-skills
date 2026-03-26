# Layout and Spacing Checklist (iOS)

Fail condition: хотя бы один layout/spacing critical не подтвержден.

## Geometry and constraints
- [ ] Подтверждены размеры контейнеров/элементов.
- [ ] Подтверждены min/max, если есть.
- [ ] Подтвержден behavior inside parent: pin/center/stretch/fixed-size.
- [ ] Подтверждена axis ownership.

## Spacing
- [ ] Padding подтвержден по каждой стороне отдельно.
- [ ] External spacing подтвержден по каждой стороне отдельно.
- [ ] Gap подтвержден явно.
- [ ] Intrinsic spacing отделен от accidental gap.

## Clipping and placement
- [ ] Подтвержден clipping origin и внутреннее размещение контента.
- [ ] Подтверждены overflow/clipping/masks.
- [ ] Подтвержден subpixel placement.

## Thin details
- [ ] Hairline/separator/stroke микро-детали подтверждены.

## Interaction
- [ ] Visual bounds подтверждены.
- [ ] Hit area подтверждена.
- [ ] Различие visual/hit bounds зафиксировано и корректно реализовано.

## Composition
- [ ] Negative space сохранен как осознанная часть композиции.
- [ ] Visual weight balance проверен дополнительно.
