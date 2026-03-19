---
name: csv-data-summarizer-claude-skill
description: CSV Data Summarizer
---

# CSV Data Summarizer Skill

## Overview
A ferramenta suprema para lidar com arquivos `.csv`. Sempre que o usuário "jogar" um arquivo CSV e pedir algo genérico (ex: "faça um resumo disso") sem especificar métricas exatas, você DEVE aplicar uma "análise cega proativa".
  
## ⚠️ Comportamento Crítico em CSVs
- **Não pergunte "o que você quer ver?".** Proceda imediatamente para a etapa de descoberta automática.
- Crie um script Python (`csv_analysis.py` ou diretamente via execução cli de REPL interativa) e inspecione:
  1. Head/Tail do dataframe (via pandas).
  2. Tipos de dados de cada coluna (DataTypes).
  3. Valores ausentes ou nulos.

## Passos para Resumo Estatístico Inteligente
Uma vez validada a integridade, extraia os principais insights do dataset:
1. **Dados Descritivos Univariados:** `.describe()` nas colunas numéricas (Média, Mediana, Desvio Padrão, Ouliers).
2. **Dados Categóricos:** Frequência de itens únicos (Count, Unique, Top, Freq) nas principais 2 colunas não-numéricas.
3. **Tendências e Correlação:** 
    - Existe dependência clara entre duas variáveis vitais (ex: 'Idade' x 'Salário'? 'Data' x 'Vendas'?).
    - Imprima outputs chave para a sua janela de leitura.

## Output ("A Entrega")
Sintetize essas informações em um relatório textual em painéis claros:
- **Resumo do Dataset.** (Total de linhas, colunas tratáveis, qualidade da base).
- **As "Três Metricas Primordiais"** (o que mais salta aos olhos).
- **Distribuições / Correlações Notáveis.**
- **Visão Visual:** (Opcional, se solicitado, gere o script de plot de um gráfico base em `exports/` via Matplotlib/Seaborn e informe ao usuário onde está o arquivo `PNG`/`PDF`).
