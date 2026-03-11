---
name: slo-implementation
description: Definição e aplicação de SLO/SLI para serviços do workspace com foco em confiabilidade, metas claras e monitoramento contínuo.
---
# SLO Implementation

## Quando usar
Usar para formalizar objetivos de confiabilidade e critérios de alerta com base em impacto real.

## Procedimento
1) Definir SLI útil (disponibilidade, latência, erro).
2) Estabelecer SLO alvo e janela de medição.
3) Conectar SLO a monitoramento e alarme.
4) Revisar periodicamente com dados reais.

## Restrições DOC2.5
- Não criar SLO sem fonte de métrica confiável.
- Evitar metas sem dono e sem plano de ação.
- Commit só por ordem do PO.

## Dependências
- Métricas instrumentadas
- Dashboard/alerting configurado
