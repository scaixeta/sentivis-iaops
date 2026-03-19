---
name: playwright-skill
description: Playwright Browser Automation Executer
---

# Playwright Browser Automation Skill

## Overview
Esta skill dita o fluxo para você escrever scripts do `Playwright` e testar páginas web, sistemas e fluxos complexos. Em vez de integrar uma IDE externa, o fluxo deve ser de criação dinâmica de roteiros transientes em diretórios correntes.

## Workflow Crítico

### Passo 1: Detectar Servidores e Definir o Alvo
Sempre certifique-se da URL base da aplicação.
- Ela está rodando localmente (ex: `localhost:3000`)? Se houver múltiplos, pergunte ao usuário.
- O sistema já possui um servidor acessível na mesma rede?

### Passo 2: Escrever o Teste num Diretório Temporário
- **NÃO grave os arquivos de teste `.js` no diretório da skill ou no repositório final, ao menos que seja explicitamente solicitado** (ex: no formato Jest/Mocha config finais).
- Se a intenção é só testar/depurar uma funcionalidade interativamente para aprovar o "Go-Live", salve como `/tmp/playwright-test-*.js`.

### Passo 3: Configuração do Automação (Headless vs Visible)
- SEMPRE inicie o browser num estado visual para testes do usuário local (depuração), ou seja `headless: false`, a menos que o usuário solicite explicitamente "rode background/headless".
- Isso permite que o desenvolvedor acompanhe a execução.
```javascript
// Exemplo em script /tmp/playwright-test-page.js
const { chromium } = require('playwright');
const TARGET_URL = 'http://localhost:3001';

(async () => {
    const browser = await chromium.launch({ headless: false }); // <-- CRÍTICO
    const page = await browser.newPage();
    await page.goto(TARGET_URL);
    // ...
})();
```

### Passo 4: Execução
Rode o script criado usando `node /tmp/playwright-test-page.js` no terminal ativo. Exiba os outputs capturados para o usuário através da ferramenta de comunicação normal ou via captura de screenshot/PDF (caso programado na automação do Playwright).

### Casos Comuns:
1. **Teste Responsivo** (Viewports Múltiplas)
2. **Identificação de Links Quebrados**
3. **Teste Lógico Completo de Login/Métricas**

Sempre prepare o código para tirar uma _screenshot em caso de falha (`.catch`)_ para auditar erros nos seletors UI.
