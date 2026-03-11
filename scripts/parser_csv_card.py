import csv
import json
import re
import sys
from pathlib import Path

def parse_csv_card(file_path):
    """
    Realiza o parse de Fatura de Cartao em CSV (padrao Itau).
    Colunas: data, lançamento, valor
    Avalia a presenca de parcelas (ex: 01/02) no campo lancamento.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

    transactions = []
    
    with open(path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2): # Headers is 1
            raw_date = row.get('data', '').strip()
            raw_desc = row.get('lançamento', '').strip()
            raw_amt = row.get('valor', '').strip()
            
            if not raw_date or not raw_amt:
                continue
                
            txn = {
                "raw_line_ref": f"row:{row_num}",
                "txn_date": raw_date,
                "description_raw": raw_desc,
                "amount": float(raw_amt),
                "installment_current": None,
                "installment_total": None
            }
            
            # Busca padrao de parcela RR/TT no final do texto
            # Ex: "MERCADOLIVRE*7PROD02/02" ou "MERCADOLIVRE*7PROD 02/02"
            match = re.search(r'(\d{2})/(\d{2})$', raw_desc)
            if match:
                txn['installment_current'] = int(match.group(1))
                txn['installment_total'] = int(match.group(2))
                
            transactions.append(txn)

    return transactions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parser_csv_card.py <caminho_para_arquivo_csv>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        txns = parse_csv_card(file_path)
        print(json.dumps(txns, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
