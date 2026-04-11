# Embrapa — Base de Conhecimento

> Consolidado diretamente da Embrapa CNPTIA AgroAPI (Agritec v2), confirmado em abril de 2026.
> Subtópicos: [Café](./cultura.md)

---

## 1. O Que É

A **Embrapa CNPTIA** (Centro Nacional de Pesquisa de Informática Agropecuária) disponibilza a **AgroAPI**, uma plataforma de APIs agronômicas construída sobre WSO2 API Manager. A API de interesse para o projeto café é a **Agritec v2**.

| Item | Valor |
|---|---|
| Base URL | `https://api.cnptia.embrapa.br` |
| Context | `/agritec/v2` |
| Autenticação | OAuth 2.0 — client_credentials |
| Plano | Gratuito (1.000 chamadas/mês) |

---

## 2. Autenticação

A API exige token Bearer gerado a cada chamada, com scope `PRODUCTION`.

**Nunca usar token genérico — ele não funciona nesta API.**

```bash
AUTH=$(echo -n "yv2EkM5NxzOSU_hiQEFEPKY8KbIa:rff_Na3U5sl5YlOHOhUn4vF4b7sa" | base64)
TOKEN=$(curl -k -s --max-time 15 -X POST \
  -d "grant_type=client_credentials&scope=PRODUCTION" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  "https://api.cnptia.embrapa.br/token" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

Depois, usar em todas as chamadas:
```
-H "Authorization: Bearer $TOKEN"
```

**Escopo obrigatório:** `PRODUCTION`. Com `default` ou ausente, a API retorna 401 em vários endpoints.

**Validade do token:** 3.600 segundos (1 hora). Para chamadas em batch, gerar token sob demanda.

**Credenciais — NÃO versionar:**
```
EMBRAPA_CONSUMER_KEY=yv2EkM5NxzOSU_hiQEFEPKY8KbIa
EMBRAPA_CONSUMER_SECRET=rff_Na3U5sl5YlOHOhUn4vF4b7sa
EMBRAPA_TOKEN_URL=https://api.cnptia.embrapa.br/token
```
Local: `C:\CindyAgent\.scr\.env`

---

## 3. Endpoints Testados

| Endpoint | Status | Parâmetros | Resposta |
|---|---|---|---|
| `GET /culturas` | OK | Nenhum | 46 culturas disponíveis |
| `GET /municipios` | OK | Nenhum | 5.573 municípios com lat/long |
| `GET /municipios/{codigoIBGE}` | Não testado | — | — |
| `GET /municipios/{codigoIBGE}/culturas` | Vazio | — | Base vazia |
| `GET /zoneamento` | OK | `idCultura`, `codigoIBGE` (obrigatórios), `riscos` (opcional) | Períodos de plantio, solo, risco, portaria |
| `GET /cultivares` | Sem dados | `idCultura` + `uf` | Nenhuma cultivar associada a café |
| `GET /obtentores` | OK | Nenhum | 101 obtentores/mantenedores |
| `GET /produtividade` | Sem dados | Exige `idCultura` + `idCultivar` simultaneamente | Café sem cultivares → sem produtividade |

---

## 4. O Que Não Existe Neste Context

Os endpoints abaixo retornaram **404 — não existem** na Agritec v2:
- `producao`, `UnidadeProducao`, `previsao-tempo`, `climaticos`
- `regioes`, `tiposSolo`, `tiposClima`, `solo`, `clima`, `unidadesMedida`

Para esses dados, é necessário buscar diretamente no site da Embrapa Café ou no Observatório do Café.

---

## 5. Base de Dados — Características

| Item | Valor |
|---|---|
| Atualização municípios | 2018-05-02 |
| Atualização zoneamento | Portaria mais recente: 582 de 16/12/2021 |
| Filtro por nome de município | Não existe — é preciso saber o código IBGE |
| Filtro por UF | Funciona apenas em `/cultivares` |

**Busca por município:** a estratégia é baixar a lista completa uma vez e filtrar localmente. Exemplo — buscar Mococa:
```bash
curl .../municipios ... | python3 -c "
import json, sys
d = json.load(sys.stdin)
for m in d['data']:
    if 'MOCOCA' in m['nome']:
        print(json.dumps(m, indent=2))
"
# Resultado: Mococa-SP = IBGE 3530508
```

---

## 6. Subtópicos

### Café
A cultura do café é tratada no arquivo [cultura.md](./cultura.md), que inclui:
- IDs das culturas de café na API
- Zoneamento com períodos de plantio e tipos de solo
- O que a API entrega e o que não entrega para café
- Dados de produção brasileira (CONAB/Embrapa 2025)

---

## 7. Validações

| Item | Status |
|---|---|
| Autenticação scope=PRODUCTION | Validado |
| Zoneamento com código real | Validado (Mococa SP) |
| Parâmetro correto: `idCultura` | Confirmado (não é `culturaId`) |
| Cultivares de café | Ausente na base |
| Produtividade de café | Sem dados (depende de cultivares) |

---

## 8. Pendências

- [ ] Mapear zoneamento para municípios de MG, ES, RO, AM
- [ ] Descobrir base externa de variedades de café (RNC/MAPA)
- [ ] Buscar dados de produtividade histórica no site da Embrapa Café
- [ ] Montar script Python para gerenciar tokens e chamadas em batch
- [ ] Salvar lista de 5.573 municípios em arquivo local para consulta sem API

---

*Atualizado em: abril de 2026*
*Fonte: Embrapa CNPTIA AgroAPI — Agritec v2 — extração direta*
