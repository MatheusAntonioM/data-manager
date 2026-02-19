import re
from typing import Dict


def analisar_texto(texto: str, nome_arquivo: str) -> Dict:

    match_cpf = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
    cpf = match_cpf.group(0) if match_cpf else "CPF_NAO_DETECTADO"

    match_nome = re.search(r"(?:Nome|Cliente)\s*[:]?\s*(.+)", texto, re.IGNORECASE)
    nome = match_nome.group(1).strip() if match_nome else "NOME_NAO_DETECTADO"

    return {
        "Arquivo Original": nome_arquivo,
        "Nome Completo": nome.upper(),
        "CPF": cpf,
        "Status": "OK" if match_cpf else "REVISAR",
    }
