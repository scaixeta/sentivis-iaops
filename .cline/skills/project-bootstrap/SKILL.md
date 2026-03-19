---
name: project-bootstrap
description: Inicializar projeto novo a partir do baseline de geracao. Use quando o pedido for criar projeto, montar estrutura basica ou bootstrap DOC2.5.
---

# Skill: Bootstrap de Projeto DOC2.5

Use esta skill quando o pedido envolver criacao de projeto novo a partir de um repositorio que contenha `Templates/`, `rules/WORKSPACE_RULES.md` e `Cindy_Contract.md`, mas que ainda NAO tenha `README.md`, `Dev_Tracking.md` ou `docs/` finais materializados.

## Fase 1: Leitura Obrigatoria (NAO PULE)

Leia exatamente nesta ordem. Nao leia nada alem disso antes de explicar o plano.

1. `rules/WORKSPACE_RULES.md`
2. Regra global do runtime ativo (ex: `.clinerules/WORKSPACE_RULES_GLOBAL.md`)
3. `Cindy_Contract.md`
4. `Templates/README.md`

Apos ler esses 4 arquivos, PARE. Nao crie nenhum arquivo ainda.

## Fase 2: Apresentar Plano e Pedir Aprovacao

Apresente o plano curto ao PO e pergunte apenas: "Aprova?"

O plano deve conter:
- **O que sera criado**: os 9 artefatos canonicos (8 arquivos + Sprint/)
- **O que ficara como `Pendente de validacao`**: tudo que o PO nao disse

NAO pergunte detalhes tecnicos ("que tipo de projeto?", "qual hardware?", "quer que eu crie?").
Pedido generico = execucao generica com `Pendente de validacao`.
Detalhes tecnicos serao definidos pelo PO em conversas futuras, NAO agora.

Se o PO disser apenas um tema vago (ex: "IoT", "web app", "automacao"), voce NAO pode promover como fato:
- sensores, protocolos, hardware, backend, dashboard, integracoes, frameworks

Tudo isso deve ficar como `Pendente de validacao` ate o PO confirmar.

## Fase 3: Materializar os Artefatos Canonicos

Crie EXATAMENTE estes arquivos e diretorios:

1. `README.md`
2. `Dev_Tracking.md`
3. `Dev_Tracking_S1.md`
4. `docs/SETUP.md`
5. `docs/ARCHITECTURE.md`
6. `docs/DEVELOPMENT.md`
7. `docs/OPERATIONS.md`
8. `tests/bugs_log.md`
9. `Sprint/` (diretorio vazio para sprints encerradas)

### Como Preencher os Placeholders

Para CADA placeholder `{{VAR}}` dos templates:

| Situacao | O que fazer |
|---|---|
| O PO disse explicitamente | Usar o valor real |
| E possivel inferir com seguranca | Usar o valor e marcar como `inferido` |
| O PO nao disse e nao da para inferir | Usar `Pendente de validacao` |
| O template pede lista e nao ha dados | Colocar apenas 1 item com `Pendente de validacao` |

### Regras de Escrita

- NAO copie o template inteiro para o documento final. Use a ESTRUTURA do template, preencha com o MINIMO util.
- NAO repita governanca DOC2.5 em todos os documentos. Cada documento tem papel distinto.
- NAO infle o README com secoes de regras, estrutura canonica ou politicas. O README e um entry point curto.
- Mantenha cada documento com o menor tamanho que ainda preserve coerencia.
- Se uma secao do template nao tem dado real, OMITA a secao ou reduza a 1 linha com `Pendente de validacao`.

### Rodape do README

O bloco `## Cindy — Orquestradora (Context Router)` no final do `README.md` e FIXO e IMUTAVEL.
Copiar LITERALMENTE do template. NAO alterar texto, imagem, largura ou formatacao.
O comentario `<!-- RODAPE FIXO -->` do template e instrucao interna; NAO incluir no arquivo final gerado.

### Plataforma

- Em ambiente Windows: usar SOMENTE PowerShell nos exemplos de comando.
- Proibido: `ls`, `cat`, `rm`, `pwd`, `mkdir`, `mkdir -p`, `touch`, `grep`, `cd`.
- ATENCAO: `mkdir -p` em Windows cria uma pasta chamada `-p`. NUNCA usar.
- Proibido: blocos de codigo com linguagem `bash`. Usar `powershell` ou `text`.
- Para criar diretorios: usar `New-Item -ItemType Directory` ou deixar o runtime criar automaticamente via write_to_file.
- Usar: `Get-ChildItem`, `Get-Content`, `Remove-Item`, `Set-Location`, `New-Item`, `Select-String`.
- Se a plataforma nao estiver definida: usar linguagem neutra (sem comandos de nenhuma plataforma).
- NAO inventar secoes de `git clone` ou preparacao de ambiente que nao existam no template.

### Timestamp UTC

Formato canonico DOC2.5 (ISO 8601, 24h): `YYYY-MM-DDTHH:MM:SS-ST` para inicio e `YYYY-MM-DDTHH:MM:SS-FN` para fim.

NUNCA usar o formato compacto legado (`DDDMMDDYYYYHHMMSSAM/PMST`). Usar SOMENTE ISO 8601.

Exemplo de conversao:
- Data real: Segunda-feira, 17 de marco de 2026, 21:04:51
- Timestamp DOC2.5: `2026-03-17T21:04:51-ST`

Exemplo na tabela de tracking:
```
Event | Start | Finish | Status
---|---|---|---
ST-S1-01 | 2026-03-17T21:04:51-ST | 2026-03-17T21:15:00-FN | Done
```

Registrar no tracking SOMENTE eventos que realmente aconteceram.

## Fase 4: Validacao Final

Antes de reportar conclusao, verificar:

- [ ] Todos os 8 arquivos existem?
- [ ] Nenhum arquivo usa comandos Bash/Linux?
- [ ] Nenhum campo foi inventado sem base do PO?
- [ ] Os Timestamps estao no formato DOC2.5?
- [ ] `README.md` esta curto e focado?
- [ ] `bugs_log.md` registra pelo menos o teste de validacao estrutural?
- [ ] Existe coerencia cruzada entre README, Dev_Tracking, Dev_Tracking_S1 e bugs_log?

### Score de Qualidade

Atribuir nota de 0 a 100:

- `0-49`: ruim, nao conforme
- `50-79`: parcial, nao aprovado
- `80-100`: aprovado

A Cindy so pode considerar "estrutura inicial concluida" se a nota for >= 80.

Se a nota ficar abaixo de 80, listar os gaps objetivos antes de concluir.

## Referencias

- `rules/WORKSPACE_RULES.md`
- `Templates/README.md`
- `Cindy_Contract.md`
- `references/template-field-guide.md`
