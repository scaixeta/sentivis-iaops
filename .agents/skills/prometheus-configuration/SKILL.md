---
name: prometheus-configuration
description: Configuração de coleta de métricas com Prometheus para monitorar serviços críticos e suportar SLI/SLO.
---
# Prometheus Configuration

## Quando usar
Usar para configurar scraping, regras e organização de métricas de serviços.

## Procedimento
1) Definir targets e labels por serviço.
2) Validar qualidade e cardinalidade das métricas.
3) Criar regras de alerta objetivas.
4) Conectar métricas a dashboards de operação.

## Restrições DOC2.5
- Não adicionar métricas sem utilidade operacional.
- Evitar cardinalidade explosiva.
- Commit por comando do PO.

## Dependências
- Instância Prometheus acessível
- Endpoints `/metrics` dos serviços
