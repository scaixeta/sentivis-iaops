# RULE ENGINE EVALUATION - Sentivis SIM

## 1. O que e o Rule Engine

Pipeline de eventos: [Device/API] -> [Rule Chain] -> [Rule Nodes] -> [Actions]

## 2. Casos de Uso

| Caso | Trigger | Action |
|---|---|---|
| Temperature High | temperature > 40 | Create Alarm |
| Temperature Low | temperature < 5 | Create Alarm |
| Device Offline | sem telemetria > 5min | Create Alarm |

## 3. Comparacao: Rule Engine vs n8n

| Aspecto | Rule Engine | n8n |
|---|---|---|
| Posicao | Dentro do TB | Externo |
| Alarmes | Native | Via HTTP |
| Manutencao | TB admin | Workflow editor |

## 4. Recomendacao

Manter n8n como orquestrador principal. Rule Engine para alarmes nativos do TB dashboard.

## 5. Proximos Passos

1. Criar Rule Chain minima com alarme de temperatura
2. Testar via telemetria do device `Sentivis | 0001`
3. Validar visualizacao de alarmes no dashboard
