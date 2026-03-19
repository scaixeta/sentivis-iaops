---
name: postgres-best-practices
description: Postgres Best Practices & Optimization (Supabase)
---

# Postgres Best Practices Skill

## Overview
Esta skill compila diretrizes essenciais de otimização de performance do PostgreSQL, com curadoria baseada nas recomendações da Supabase e documentação oficial (PostgreSQL Wiki). Funciona como o guia mestre ao projetar, revisar ou otimizar bancos relacionais no ecosssistema atual.

## Categorias de Regras em Ordem de Prioridade

Sempre que atuar no Postgres (via `psql`, gerando migrations, queries `SQL` ou configurando schemas), valide seu trabalho contra as seguintes práticas em ordem decrescente de importância:

### 1. Consultas Rápidas e Eficientes (Querying)
- Use **Partial Indexes** quando filtrar por variáveis booleanas muito desbalanceadas ou domínios de pesquisa em status "ativos" (ex: `WHERE archived = false`).
- Prefira queries planejadas. Verifique sempre com `EXPLAIN ANALYZE` as predições do otimizador de plano quando a performance for crítica.
- Trate sempre Joins explosivos e identifique a viabilidade de limitadores.

### 2. Arquitetura de Conexões (Connection & Pools)
- Monitore o acúmulo de conexões se sua aplicação for serveless (functions) versus contêiners longa duração. Entenda a distinção na exigência de um PgBouncer (Pooling) nativo ou integrado via Supabase.

### 3. Modelagem de Segurança (Security & RLS)
Essencial para implementações baseadas em frameworks como Supabase que expõem o DB via API REST.
- Ative SEMPRE **Row-Level Security (RLS)** em tabelas que manipulem dados com viés multi-tenant/usuário antes de expô-las a requisições client-side.
- Crie políticas unívocas (Policies) separadas por `SELECT`, `INSERT`, `UPDATE` e `DELETE`.
- Nunca assuma que os dados confidenciais podem ser omitidos apenas filtrando na aplicação; a barreira é o banco.

### 4. Design de Esquema (Schema Design)
- Adote o uso extensivo de Constraints (`CHECK`, `FOREIGN KEYs`, `NOT NULL`) para evitar corrompimento e dívidas técnicas de aplicação. A integridade pertence ao banco.
- Cuidado com o exagero de Índices (`Index Bloat`), que atrasam os comandos `INSERT/UPDATE`. Não crie índices "por medo".

### 5. Monitoramento / Tuning Avançado
- Verifique gargalos de processadores e IO via `pg_stat_statements`.
- Saiba do comportamento de vacuuming (Blobs) em tabelas extremamente mutáveis.

## Casos de Uso
1. Escrevendo/Otimizando SQL bruto.
2. Desenhando Schemas para Novos Módulos.
3. Revisando Migrations antes de Submetê-las ao Repositório ou Executar via CI/CD.

## Ref. Oficiais Adicionais
* [Supabase Database Overview](https://supabase.com/docs/guides/database/overview)
* [Performance Optimization Psql Wiki](https://wiki.postgresql.org/wiki/Performance_Optimization)
