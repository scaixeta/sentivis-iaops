# Dev_Tracking - Sprint S5 (Sentivis IAOps)

## 1. Identificação da Sprint

| Campo | Valor |
|---|---|
| Sprint | S5 |
| Projeto | Sentivis IAOps |
| Início | 2026-04-11T00:30:00-ST |
| PO | Pendente de validação formal |

## 2. Contexto

- S4 encerrada com baseline Cirrus completo (telemetria validada, 12/12 coletas)
- S3 fechou com contrato de telemetria, modelagem, dashboard, Jira sync
- Objetivo S5: iniciar estudos de domínio agrícola — foco em café — usando Embrapa Agritec v2 API como fonte primária de dados

## 3. Escopo

Estudo de domínio de café para informar o agrônomo especialista (Team Café). Captação de dados estruturados via Embrapa Agritec v2, mapeamento de zoneamento e variedades. Entrega: KB/agro populada e baseline de conhecimento咖啡 para o agrônomo.

## 4. Backlog

| Estado | SP | Estória |
|---|---:|---|
| To-Do | — | ST-S5-01 — Mapear zoneamento咖啡 para municípios de MG, ES, RO, AM via Embrapa Agritec v2 |
| To-Do | — | ST-S5-02 — Descobrir base externa de variedades de café (RNC/MAPA) |
| To-Do | — | ST-S5-03 — Buscar dados de produtividade histórica no site da Embrapa Café |
| To-Do | — | ST-S5-04 — Montar script Python para gerenciar tokens e chamadas em batch na Embrapa API |
| To-Do | — | ST-S5-05 — Salvar lista de 5.573 municípios em arquivo local para consulta sem API |
| Done | — | ST-S5-06 — Copiar KB Embrapa/café de `{CindyAgent}/KB/` para `Sentivis SIM/KB/agro/` (embrapa.md + cultura.md) |

## 5. Decisões

| ID | Descrição | Data |
|---|---|---|
| D-S5-01 | KB de Embrapa/café copiada do CindyAgent para Sentivis SIM — não pertence ao CindyAgent | 2026-04-11 |
| D-S5-02 | Agrônomo especialista em cafés: nome não definido ainda | 2026-04-11 |
| D-S5-03 | Fluxo Team Café: estudo domínio → captação Embrapa + Firecrawl → entrega agrônomo | 2026-04-11 |

## 6. Referências

- `KB/agro/embrapa.md` — dados da Embrapa Agritec v2 API
- `KB/agro/cultura.md` — cultura do café, variedades e zoneamento

## 7. Timestamp UTC

| Event | Start | Finish | Status |
|---|---|---|---|
| ST-S5-06 | 2026-04-11T00:20:00-ST | 2026-04-11T00:25:00-FN | Done |

## 8. Regra de Commits

- Commit e push apenas sob ordem expressa do PO
