# exclusions.md - ThingsBoard CE Import Exclusions

## Status

- import_status: executed
- import_mode: selective import
- import_date_utc: `2026-03-12T23:12:53Z`

## Applied exclusion rules

| Pattern | Reason |
|---------|--------|
| `**/pe/**` | Professional Edition content |
| `**/cloud/**` | Cloud-only scope |
| `**/edge/**` | Edge-only scope |
| `**/*.png` `**/*.jpg` `**/*.svg` | Non-text assets |
| `**/*.sh` | Scripts auxiliares fora da camada KB |
| `docs/**` wrappers | Non-substantive navigation pages |

## Notes

- Regras aplicadas na importação seletiva concluída em `2026-03-12T23:12:53Z`.
- Apenas markdown CE das trilhas aprovadas foi copiado.
