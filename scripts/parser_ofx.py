import json
import re
import sys
from pathlib import Path

def parse_ofx(file_path):
    """
    Realiza o parse basico de um arquivo OFX extraindo as transacao bancarias.
    Ignora cabecalhos complexos e foca na tag <STMTTRN>.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

    # Lendo o arquivo usando codificacao dependendo do sistema (usualmente latim ou utf-8)
    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        content = path.read_text(encoding='latin-1')
        
    transactions = []
    
    # regex para encontrar todos blocos de transacao <STMTTRN>...</STMTTRN>
    # O OFX antigo nao fecha tags as vezes, mas as transacoes geralmente tem quebra de linha.
    # vamos tentar achar o bloco <STMTTRN>
    txn_blocks = re.findall(r'<STMTTRN>(.*?)(?:</STMTTRN>|<STMTTRN>|</BANKTRANLIST>)', content, re.DOTALL | re.IGNORECASE)
    
    for block in txn_blocks:
        txn = {}
        
        # Tipos comuns de OFX:
        # <TRNTYPE>CREDIT
        # <DTPOSTED>20230101120000[-3:BRT]
        # <TRNAMT>150.00
        # <FITID>123456789
        # <MEMO>PIX RECEBIDO
        
        match_type = re.search(r'<TRNTYPE>([^<>\r\n]+)', block, re.IGNORECASE)
        match_date = re.search(r'<DTPOSTED>([^<>\r\n]+)', block, re.IGNORECASE)
        match_amt = re.search(r'<TRNAMT>([^<>\r\n]+)', block, re.IGNORECASE)
        match_fitid = re.search(r'<FITID>([^<>\r\n]+)', block, re.IGNORECASE)
        match_memo = re.search(r'<MEMO>([^<>\r\n]+)', block, re.IGNORECASE)
        
        if match_fitid and match_amt:
            txn['fitid'] = match_fitid.group(1).strip()
            txn['trn_type'] = match_type.group(1).strip() if match_type else 'UNKNOWN'
            txn['amount'] = float(match_amt.group(1).strip())
            txn['date_posted'] = match_date.group(1).strip() if match_date else None
            txn['memo'] = match_memo.group(1).strip() if match_memo else ''
            transactions.append(txn)

    return transactions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parser_ofx.py <caminho_para_arquivo_ofx>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        txns = parse_ofx(file_path)
        print(json.dumps(txns, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
