---
name: observability-engineer
description: Padrões de monitoramento, logging e tracing para projetos MCP com foco em diagnóstico rápido e operação confiável.
---
# Observability Engineer

## Quando usar
Usar para definir ou revisar telemetria, health checks, métricas de serviço e análise de incidentes.

## Procedimento
1) Mapear sinais essenciais: logs, métricas, traces.
2) Definir painéis/alertas mínimos por serviço crítico.
3) Validar qualidade de logs para troubleshooting.
4) Registrar evidências e riscos operacionais.

## Restrições DOC2.5
- Não introduzir stack nova sem justificativa técnica.
- Manter foco em sinais acionáveis.
- Commit apenas por comando do PO.

## Dependências
- Acesso aos serviços e logs
- Runbooks em `docs/OPERATIONS.md`
