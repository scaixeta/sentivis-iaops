import sys
import json
import re
from pathlib import Path
try:
    import fitz # PyMuPDF
except ImportError:
    print(json.dumps({"error": "pymupdf is required."}))
    sys.exit(1)

def classify_pdf(file_path):
    """
    Quality Gate (Camada 1): Identifica se o PDF e textual ou scaneado.
    Avalia o volume de texto das primeiras paginas.
    """
    doc = fitz.open(file_path)
    text = ""
    # Pega texto das primeiras 3 paginas no maximo para amostragem
    for i in range(min(3, len(doc))):
        text += doc[i].get_text()
    
    # Se menos de 100 caracteres extraidos, provavelmente trata-se de imagem (Scan)
    classification = "TEXTUAL" if len(text.strip()) > 100 else "SCAN"
    return classification, text, doc

def parse_pdf_card(file_path):
    """
    Realiza extracao de cabecalho e linhas de fatura a partir de PDF textual.
    Retorna a classificacao e os dados estruturados para Staging.
    """
    classification, sample_text, doc = classify_pdf(file_path)
    
    if classification == "SCAN":
        return {
            "classification": "SCAN",
            "error": "OCR needed. This is a scanned PDF.",
            "header": {},
            "transactions": []
        }
        
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    transactions = []
    header = {}
    
    # 1. Extracao de Cabecalho Generico de Fatura
    # Padrão: Vencimento(es) DD/MM/AAAA ou Total R$ 1.234,56
    due_date_match = re.search(r'(?:vencimento|vende em).*?(\d{2}/\d{2}/\d{2,4})', full_text, re.IGNORECASE | re.DOTALL)
    if due_date_match:
        header['due_date'] = due_date_match.group(1)
        
    total_match = re.search(r'(?:total.*?fatura|valor.*?pagar).*?(?:r\$)\s*([0-9.,]+)', full_text, re.IGNORECASE | re.DOTALL)
    if total_match:
        val_str = total_match.group(1).replace('.', '').replace(',', '.')
        header['total_amount'] = float(val_str)
        
    # 2. Extracao de Transacoes iterando linhas
    # O PyMuPDF no Itau quebra: Data \n Desc \n Valor
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    state = 0
    current_txn = {}
    date_pattern = re.compile(r'^(\d{2}/\d{2}(?:/\d{2,4})?)$')
    
    for line in lines:
        if state == 0:
            match_date = date_pattern.search(line)
            if match_date:
                current_txn['txn_date'] = match_date.group(1)
                state = 1
        elif state == 1:
            current_txn['description_raw'] = line
            state = 2
        elif state == 2:
            # O proximo item pode ser o valor OU a categoria (ex: "ALIMENTACAO").
            # Vamos checar se eh valor (-? \d+,\d{2})
            val_match = re.search(r'^-?(\d{1,3}(?:\.\d{3})*,\d{2})$', line)
            if val_match:
                amt_str = val_match.group(1).replace('.', '').replace(',', '.')
                # Detectar credito (em PDF muitas vezes vem com - na frente ou apenas normal e depende de credito)
                # Vamos assumir o valor float direto:
                amt = float(amt_str)
                if line.startswith('-'):
                    amt = -amt
                current_txn['amount'] = amt
                
                # Tratar parcelas no description
                desc = current_txn['description_raw']
                inst_curr, inst_tot = None, None
                inst_match = re.search(r'(\d{2})/(\d{2})$', desc)
                if inst_match:
                    inst_curr = int(inst_match.group(1))
                    inst_tot = int(inst_match.group(2))
                    
                current_txn['installment_current'] = inst_curr
                current_txn['installment_total'] = inst_tot
                
                transactions.append(current_txn.copy())
                state = 0
                current_txn = {}
            else:
                # Se nao achamos um valor, ignoramos ou resetamos (ex: ignorando lixos no meio)
                # As vezes a categoria entra no meio, mas normalmente a Data recomeca.
                # Se for data novamente, recomeca:
                if date_pattern.search(line):
                    current_txn = {'txn_date': date_pattern.search(line).group(1)}
                    state = 1
            
    return {
        "classification": classification,
        "header": header,
        "transactions": transactions
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parser_pdf_card.py <caminho_para_arquivo_pdf>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        data = parse_pdf_card(file_path)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
