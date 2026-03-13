# rule-engine-first-check.md

## Objective
Executar checagem inicial de rule chain para eventos básicos de telemetry.

## When to use
Quando a ingestão ocorre, mas ação esperada de regra não dispara.

## Preconditions
- Rule chain configurada e vinculada.
- Permissão para visualizar logs/eventos.

## Short steps
1. Abrir configuração do Rule Engine.
2. Confirmar chain root ativa.
3. Verificar nós críticos e últimos eventos.

## Common errors
- Chain não publicada/ativada.
- Filtro de mensagem incompatível com payload.

## Internal references
- `send-http-telemetry.md`
- `troubleshooting-ingestion.md`

## Out of scope
Modelagem avançada de automações multi-chain.
