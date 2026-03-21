# FR — Modelo de Valor (Fibonacci 1–21) por Observação (Candidato a Canônico)

- Projeto: Sentivis IAOps (Sentivis SIM workspace)
- Artefato: Feature Request (FR)
- Status: Candidato a canônico (provisório)
- Base: Observação empírica a partir de Dev_Tracking (DOC2.5)
- Data (local): 2026-03-20

## 1) Objetivo

Padronizar um modelo de estimativa/valor em Fibonacci (1 a 21) baseado em observação do histórico real do time, usando os `Dev_Tracking_SX.md` como fonte de evidência (timestamps, fluxo do backlog e carryover).

Este documento define:

- O que medir nos `Dev_Tracking`
- Como medir (processo reprodutível)
- Uma primeira calibração de escala Fibonacci 1–21 para o time
- Como aplicar na prática, com ancoras observadas

## 2) O Que Foi Entendido (Contexto do PO)

- O PO quer calibrar Story Points (Fibonacci 1–21) por observação do que o time realmente executa, não por teoria.
- Como estamos na Sprint S2, já existe histórico suficiente para propor uma primeira escala.
- O modelo deve nascer de evidências: tempo registrado + atrito/complexidade percebida no fluxo (carryover, CRs, testes, integrações).

## 3) Fontes de Evidência (Arquivos)

- `Dev_Tracking.md` (índice de sprints)
- `Sprint/Dev_Tracking_S0.md`
- `Sprint/Dev_Tracking_S1.md`
- `Dev_Tracking_S2.md` (sprint ativa)

Sinal explorado em cada sprint:

- `## 3. Backlog da Sprint` (contagem por status, carryover)
- `## 6. Timestamp UTC` (duração observável por item com Start/Finish)

## 4) Como o Processo Foi Realizado (Detalhado e Reprodutível)

Passos executados (inspeção local):

- Listar arquivos de tracking: `ls -1 Dev_Tracking*.md` e `ls -1 Sprint`
- Ler o índice: `sed -n '1,220p' Dev_Tracking.md`
- Ler sprints encerradas: `sed -n '1,240p' Sprint/Dev_Tracking_S0.md` e `sed -n '1,220p' Sprint/Dev_Tracking_S1.md`
- Ler a seção de timestamps da sprint ativa: `sed -n '96,160p' Dev_Tracking_S2.md`
- Confirmar presença das seções canônicas: `rg -n "^## 6\\. Timestamp UTC" Sprint/Dev_Tracking_S0.md Sprint/Dev_Tracking_S1.md Dev_Tracking_S2.md`

Extração/medição (script ad-hoc, sem alterar repositório):

- Parse da tabela `Timestamp UTC` e cálculo de duração em minutos por evento com `Start` e `Finish`.
- Filtragem de itens de trabalho: `ST-*` e `CR-*`, excluindo `Pending-*`.
- Parse da tabela `Backlog` para contagem por status.
- Cálculo de distribuição (mediana, p75, p90, max) e buckets por duração.

Script usado (reprodutível):

```python
from pathlib import Path
import re
from datetime import datetime
from collections import defaultdict
from statistics import median

FILES = [
    Path("Sprint/Dev_Tracking_S0.md"),
    Path("Sprint/Dev_Tracking_S1.md"),
    Path("Dev_Tracking_S2.md"),
]

def parse_dt(s: str):
    s = s.strip()
    if s == "-" or not s:
        return None
    if s.endswith("-ST") or s.endswith("-FN"):
        s = s[:-3]
    return datetime.fromisoformat(s)

def infer_sprint_name(path: Path):
    m = re.search(r"_S(\d+)\.md$", path.name)
    return f"S{m.group(1)}" if m else path.stem

def parse_timestamp_rows(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    sprint = infer_sprint_name(path)

    in_ts = False
    in_table = False
    rows = []

    for line in lines:
        if line.strip().lower() == "## 6. timestamp utc":
            in_ts = True
            continue
        if in_ts and line.strip().startswith("Event | Start | Finish | Status"):
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("---|"):
                continue
            if not line.strip():
                break
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4:
                continue
            event, start, finish, status = parts[:4]
            rows.append(
                (sprint, event.strip(), parse_dt(start), parse_dt(finish), status.strip())
            )
    return rows

def parse_backlog_items(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    sprint = infer_sprint_name(path)
    items = []
    in_table = False

    for line in lines:
        if line.strip().lower().startswith("| status | est"):
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("|---") or line.strip().startswith("|--------"):
                continue
            if not line.strip():
                break
            if "|" not in line:
                break
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 2:
                items.append((sprint, parts[0], parts[1]))
    return items

rows = []
for f in FILES:
    rows.extend(parse_timestamp_rows(f))

work = []
for sprint, event, st, fn, status in rows:
    kind = event.split("-")[0] if "-" in event else event
    if kind not in ("ST", "CR"):
        continue
    if status.lower().startswith("pending"):
        continue
    if not st or not fn:
        continue
    dur_min = (fn - st).total_seconds() / 60
    work.append((sprint, event, status, dur_min))

durations = sorted([d for *_rest, d in work])

def pct(p):
    if not durations:
        return None
    idx = int(round((p / 100) * (len(durations) - 1)))
    return durations[idx]

print("count", len(durations))
print("min", min(durations))
print("median", median(durations))
print("p75", pct(75))
print("p90", pct(90))
print("max", max(durations))

backlog = []
for f in FILES:
    backlog.extend(parse_backlog_items(f))

counts = defaultdict(lambda: defaultdict(int))
totals = defaultdict(int)
for sprint, status, _story in backlog:
    counts[sprint][status] += 1
    totals[sprint] += 1

for sprint in sorted(counts.keys()):
    print(sprint, totals[sprint], dict(counts[sprint]))
```

Limitações explícitas:

- `Timestamp UTC` mede “tempo observado entre start/finish”, não garante tempo efetivo (pode capturar espera/execução longa ou apenas marcação).
- Valores `0m` acontecem quando `Start == Finish` (logging instantâneo).
- A calibração é “primeira versão” e deve ser revisada ao acumular mais eventos na S2/S3.

## 5) Relatório (Na Íntegra)

Entendi que você quer “calibrar” Story Points (Fibonacci 1–21) por observação do que o time realmente executa e do atrito/complexidade que aparece nos nossos `Dev_Tracking` (e não por teoria).

Eu avaliei estes tracks: `Sprint/Dev_Tracking_S0.md`, `Sprint/Dev_Tracking_S1.md`, `Dev_Tracking_S2.md` (e o índice `Dev_Tracking.md`) e extraí dois sinais bem objetivos: (1) fluxo do backlog e carryover; (2) distribuição de tempos dos eventos `ST/CR` com `Start/Finish` registrados.

1) Visão de Fluxo (Backlog)

| Sprint | Itens | Done | Pending-* (carryover) | To-Do | % Done |
|---|---:|---:|---:|---:|---:|
| S0 | 18 | 10 | 8 | 0 | 56% |
| S1 | 18 | 7 | 8 | 3 | 39% |
| S2 | 15 | 6 | 8 | 1 | 40% |

Leitura: os 8 itens herdados (ST-S0-03..ST-S0-10) ficam “pendurados” de S0 → S1 → S2; isso é um marcador de épico/tema (ou falta de fatiamento) e tende a ser onde 13/21 moram.

2) Tempos Observados (ST/CR concluídos, excluindo `Pending-*`)

Resumo (minutos): `count=23`, `mediana=5m`, `p75=10m`, `p90=15m`, `máx=376m (~6,3h)`

Distribuição:

| Bucket | Count |
|---|---:|
| 0m | 5 |
| (0,1] | 2 |
| (1,5] | 6 |
| (5,10] | 6 |
| (10,15] | 2 |
| 240m+ | 2 |

Maiores itens (âncoras reais):

- `S2 ST-S1-08` ≈ 375m (6,25h)
- `S2 CR-S1-01` ≈ 376m (6,27h)

Observacao importante:

- Estes itens de ~6h aconteceram antes da padronizacao formal de pontuacao Fibonacci no backlog (`SP`).
- Eles entram como ancora empirica para calibracao inicial (21), nao como exemplo de instrumentacao perfeita de backlog.

3) Escala Fibonacci (1, 2, 3, 5, 8, 13, 21) calibrada para este time

| Pontos | Faixa observável (heurística) | Quando usar (característica) |
|---|---|---|
| 1 | 0–5 min | operação/ajuste atômico, baixo risco, 1 passo |
| 2 | 5–10 min | pequeno ajuste com 1 verificação |
| 3 | 10–20 min | mudança pequena porém com 2+ passos/arquivos, precisa evidência mínima |
| 5 | 20–60 min | envolve decisão + ajuste + validação (ainda não apareceu muito nos timestamps) |
| 8 | 1–3 h | integrações/fluxo com mais superfície, chance real de retrabalho |
| 13 | 3–6 h | coordenação + incerteza, exige decomposição se possível |
| 21 | 6h+ ou atravessa sprint | alto risco/abrangência; obrigatório fatiar se repetível |

Por que essa lógica fecha com o histórico:

- O “miolo” do time (com apoio dos integradores e execução assistida) está concentrado em ≤ 15 min (p90), então 1–3 pontos cobrem a maior parte do trabalho rotineiro.
- Os poucos itens que “explodem” para horas (como `ST-S1-08` e `CR-S1-01`) viram nossas âncoras de 21 hoje.
- O carryover fixo (8 pendências de S0) é o sinal mais forte de que precisamos decompor para transformar “pendência eterna” em itens 3/5/8 executáveis.

## 6) Proposta de Padronização (Modelo Operacional)

Recomendação de uso (regra prática):

- Se a atividade cabe em uma sessão curta e tem baixo risco: `1–3`
- Se envolve validação e pode exigir um retorno/ajuste: `5`
- Se toca integração, mapeamento real, reconciliação, operações Jira, ou tem superfície ampla: `8`
- Se tem dependência externa, incerteza estrutural, ou requer coordenação: `13`
- Se já sabemos que atravessa sprint, ou tende a virar “pendência eterna” sem fatiamento: `21` (obrigatório quebrar em itens menores)

Critério de evidência:

- `Timestamp UTC` deve ser mantido consistente e atualizado para que a calibração continue real.
- Carryover (`Pending-SX`) é sinal de “item grande demais” ou “tema/épico sem fatiamento”.

## 7) Próximos Passos (para virar padrão)

- Adotar esta calibração como baseline de S2/S3.
- A cada sprint, recalcular:
  - mediana, p75, p90 e top-5 durações (ST/CR)
  - contagem e idade de carryovers (Pending-*)
- Se p90 subir consistentemente (ex.: > 30m), recalibrar as faixas.
- Se itens 13/21 forem recorrentes, exigir fatiamento em backlog.
