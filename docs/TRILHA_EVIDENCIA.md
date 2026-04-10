# TRILHA DE EVIDENCIA - Sentivis SIM

## 1. Fontes de Evidencia

| Ficheiro | Conteudo |
|---|---|
| Dev_Tracking.md | Indice de sprints |
| Sprint/Dev_Tracking_S3.md | Backlog e timestamps da S3 |
| tests/bugs_log.md | Log de testes e bugs |

## 2. Tipos de Evidencia

### TEST-SX-YY

Registrada em `tests/bugs_log.md`

### BUG-SX-YY

Registrada em `tests/bugs_log.md`

### D-SX-YY

Registrada em `Dev_Tracking_SX.md`

## 3. Trilha S3 - Estorias Executadas

| Estoria | SP | Estado | Evidencia |
|---|---|---|---|
| ST-S0-03 | 8 | Done | docs/TELEMETRY_CONTRACT.md |
| ST-S0-04 | 13 | Done | docs/DEVICE_PROFILE_MODELING.md |
| ST-S0-05 | 5 | Done | docs/SETUP.md ja cobria |
| ST-S0-06 | 13 | Done | docs/DASHBOARD_BASELINE.md |
| ST-S0-07 | 8 | Done | docs/RULE_ENGINE_EVALUATION.md |
| ST-S0-08 | 3 | Done | Workstation VS Code operacional |
| ST-S0-09 | 5 | Done | docs/TRILHA_EVIDENCIA.md (este) |
| ST-S0-10 | 13 | Done | docs/HARDWARE_BASELINE.md + Cirrus Lab conectado |

## 4. Trilha n8n -> ThingsBoard (validada)

```
[Mock/Script] -> [POST /webhook/device-telemetry] -> [n8n] -> [POST /api/v1/{TOKEN}/telemetry] -> [ThingsBoard]
```

Evidencia: TEST-GATE-S3-F0 (Passed, 2026-04-11)

## 5. Regras de Evidencia

1. Toda execucao de teste gera TEST-SX-YY em `tests/bugs_log.md`
2. Todo bug gera BUG-SX-YY em `tests/bugs_log.md`
3. Toda decisao gera D-SX-YY em `Dev_Tracking_SX.md`
4. Nunca apagar trilha
