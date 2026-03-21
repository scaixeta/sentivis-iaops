#!/usr/bin/env python3
"""
integrators/common/tracking_writer.py - Escrita Segura no Dev_Tracking

Atualiza apenas a coluna Jira da tabela de backlog, sem alterar
outras secoes do arquivo.

Uso:
    from integrators.common.tracking_writer import write_back_jira_keys
    write_back_jira_keys("Dev_Tracking_S2.md", item_to_jira_map)
"""

import re
from pathlib import Path
from typing import Optional


def extract_doc25_id_from_story(story_cell: str) -> Optional[str]:
    """
    Extrai o identificador principal de uma celula de estoria.
    
    Formato esperado:
    - legado: "ST-S0-03 - Titulo" ou "ST-S0-03"
    - novo/transicional: "STVIA-45 - Titulo" ou "STVIA-45"
    """
    match = re.match(r"^([A-Z]+-S\d+-\d+|[A-Z][A-Z0-9]+-\d+)", story_cell.strip())
    if match:
        return match.group(1)
    return None


def write_back_jira_keys(
    tracking_file: str,
    item_to_jira: dict[str, str],
    dry_run: bool = True
) -> dict:
    """
    Atualiza a coluna Jira na tabela de backlog do Dev_Tracking.
    
    Args:
        tracking_file: Caminho para o arquivo Dev_Tracking_SX.md
        item_to_jira: Dicionario {item_id: jira_key} ex: {"ST-S0-03": "STVIA-45"}
        dry_run: Se True, apenas mostra as mudancas sem escrever
    
    Returns:
        Dict com statisticas: {"updated": N, "skipped": N, "errors": [...]}
    """
    path = Path(tracking_file)
    if not path.exists():
        return {"error": f"Arquivo nao encontrado: {tracking_file}"}
    
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Encontrar a tabela de backlog
    header_idx = None
    header = None
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*Status\s*\|", line, flags=re.IGNORECASE) and re.search(r"Est", line, flags=re.IGNORECASE):
            header = [c.strip().lower() for c in line.strip().strip("|").split("|")]
            header_idx = i
            break
    
    if header_idx is None:
        return {"error": "Tabela de backlog nao encontrada"}
    
    # Encontrar indices das colunas
    def idx_of(pred):
        for j, name in enumerate(header):
            if pred(name):
                return j
        return None
    
    status_idx = idx_of(lambda n: n == "status") or 0
    sp_idx = idx_of(lambda n: n == "sp")
    jira_idx = idx_of(lambda n: n == "jira")
    story_idx = idx_of(lambda n: n.startswith("est"))
    if story_idx is None:
        story_idx = len(header) - 1
    
    if jira_idx is None:
        return {"error": "Coluna Jira nao encontrada na tabela"}
    
    # Processar linhas da tabela
    updated = 0
    skipped = 0
    errors = []
    new_lines = lines.copy()
    
    for i in range(header_idx + 2, len(lines)):
        line = lines[i]
        
        # Para de processar quando sair da tabela
        if not line.strip().startswith("|"):
            break
        if "---" in line:
            continue
        
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) <= max(status_idx, story_idx, jira_idx):
            continue
        
        story_cell = cols[story_idx].strip()
        doc25_id = extract_doc25_id_from_story(story_cell)
        
        if not doc25_id:
            continue
        
        # Verifica se tem mapping para este ID
        if doc25_id not in item_to_jira:
            skipped += 1
            continue
        
        jira_key = item_to_jira[doc25_id]
        current_jira = cols[jira_idx].strip() if jira_idx < len(cols) else ""
        
        # Se ja tem a mesma key, nao precisa atualizar
        if current_jira == jira_key:
            skipped += 1
            continue
        
        # Atualiza a coluna Jira
        cols[jira_idx] = jira_key
        new_line = "| " + " | ".join(cols) + " |"
        new_lines[i] = new_line
        updated += 1
    
    # Mostra plano de mudancas
    print(f"[WRITE-BACK] {updated} linhas serao atualizadas, {skipped} ignoradas")
    
    if dry_run:
        print("[DRY-RUN] Nenhuma alteracao foi escrita.")
        print("\nMudancas planejadas:")
        for i in range(header_idx + 2, len(lines)):
            if i >= len(new_lines):
                break
            old = lines[i]
            new = new_lines[i]
            if old != new:
                print(f"  {extract_doc25_id_from_story(lines[i])}: '{lines[i].split('|')[jira_idx+1].strip()}' -> '{new.split('|')[jira_idx+1].strip()}'")
        return {"updated": updated, "skipped": skipped, "dry_run": True}
    
    # Escreve o arquivo
    new_content = "\n".join(new_lines)
    path.write_text(new_content, encoding="utf-8")
    
    return {"updated": updated, "skipped": skipped, "dry_run": False}


if __name__ == "__main__":
    # Teste rapido
    import sys
    if len(sys.argv) > 1:
        # Teste com mapping vazio
        result = write_back_jira_keys(sys.argv[1], {}, dry_run=True)
        print(result)
