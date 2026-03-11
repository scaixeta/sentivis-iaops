---
name: grafana-dashboards
description: Construção de dashboards Grafana orientados a operação, incidentes e acompanhamento de saúde de serviços.
---
# Grafana Dashboards

## Quando usar
Usar para desenhar ou revisar dashboards operacionais com foco em leitura rápida e ação.

## Procedimento
1) Selecionar KPIs/SLIs essenciais.
2) Organizar painéis por serviço e criticidade.
3) Definir thresholds e links para investigação.
4) Validar dashboard em cenário normal e incidente.

## Restrições DOC2.5
- Não criar dashboard ornamental sem uso operacional.
- Priorizar legibilidade e contexto.
- Commit/push só com comando do PO.

## Dependências
- Grafana com datasource configurado
- Métricas/traces disponíveis
