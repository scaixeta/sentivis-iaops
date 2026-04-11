# Cultura — Café

> Mapeamento da cultura de café via Embrapa CNPTIA AgroAPI (Agritec v2).
> Dados extraídos e validados diretamente na API em abril de 2026.

---

## 1. Culturas Cadastradas na API

Todas as culturas de café identificadas na API. Cada uma é **perene**, com **zoneamento disponível**,
mas **sem cultivar, produtividade ou adubação** na base atual.

| ID | Nome | Cultivo | Zoneamento | Cultivar | Produtividade | Adubação |
|---|---|---|---|---|---|---|
| 114 | CAFÉ ARÁBICA IRRIGADO | Irrigado | Sim | Não | Não | Não |
| 258 | CAFÉ ARÁBICA IRRIGADO PRODUÇÃO | Irrigado | Sim | Não | Não | Não |
| 115 | CAFÉ ARÁBICA SEQUEIRO | Sequeiro | Sim | Não | Não | Não |
| 259 | CAFÉ ARÁBICA SEQUEIRO PRODUÇÃO | Sequeiro | Sim | Não | Não | Não |
| 116 | CAFÉ ROBUSTA IRRIGADO | Irrigado | Sim | Não | Não | Não |
| 117 | CAFÉ ROBUSTA SEQUEIRO | Sequeiro | Sim | Não | Não | Não |
| 1223 | CAFÉ ROBUSTA IMPLANTAÇÃO IRRIGADO | Irrigado | Sim | Não | Não | Não |
| 1224 | CAFÉ ROBUSTA IMPLANTAÇÃO SEQUEIRO | Sequeiro | Sim | Não | Não | Não |

---

## 2. Zoneamento — Parâmetros de Consulta

**Endpoint:** `GET /agritec/v2/zoneamento`

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `idCultura` | Sim | ID da cultura (tabela acima) |
| `codigoIBGE` | Sim | Código IBGE do município (7 dígitos) |
| `riscos` | Não | 20, 30 ou 40. Se omitido, retorna todos. |

**Resposta:** períodos de plantio válidos, tipo de solo, risco (%) e portaria.

---

## 3. Zoneamento — Municípios Validados

Resultados reais retornados pela API.

### Mococa — SP (IBGE 3530508)

Cultura: Café Arábica Sequeiro (id=115) | Risco: 20% | Portaria: 582 de 16/12/2021

| Solo | Início | Fim |
|---|---|---|
| Arenoso | 11/out | 10/dez |
| Argiloso | 11/out | 20/nov |
| Textura Média | 11/out | 10/dez |

---

## 4. O Que a API Não Entrega Para Café

| Módulo | Status |
|---|---|
| Cultivares | Inexistente na base (hasCultivar: false em todas) |
| Produtividade | Inexistente na base (hasProdutividade: false) |
| Adubação | Inexistente na base (hasAdubacao: false) |
| Obentores/Cultivares | 101 obtentores cadastrados na API, mas nenhum associado a café |

> **Implicação:** para dados de variedades de café, é necessário buscar fora da AgroAPI —
> diretamente no site da Embrapa Café ou em bases como o Registro Nacional de Cultivares (RNC/MAPA).

---

## 5. Produção Brasileira de Café (Contexto)

Dados de mercado para enquadramento agronômico.

| Item | Valor | Fonte |
|---|---|---|
| Produção Brasil 2025 | 51,81 milhões de sacas | Embrapa Café / CONAB, mar/2025 |
| Variação vs 2024 | Queda de 4,4% | Embrapa Café / CONAB, mar/2025 |
| Área em produção | 1,85 milhão de hectares | Embrapa Café / CONAB |
| Produtividade média | 28 sacas / hectare | Embrapa Café / CONAB |
| Participação Sudeste | 86,7% da produção (44,93M sacas) | Embrapa Café / CONAB |

---

## 6. Próximos Passos de Preenchimento

- [ ] Mapear zoneamento para municípios de MG (arábica), ES (arábica) e RO/AM (robusta)
- [ ] Preencher seção de obtentores com os 101 cadastrados na API
- [ ] Incluir dados de zoneamento para as culturas de café irrigado (114, 258, 116, 1223)
- [ ] Localizar base externa de variedades de café (RNC/MAPA ou Embrapa Café)
- [ ] Documentar práticas de cultivo e ciclo phonological a partir da literatura Embrapa

---

*Atualizado em: abril de 2026*
*Fonte primária: Embrapa CNPTIA AgroAPI — Agritec v2*
