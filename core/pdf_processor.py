from typing import Optional

import pdfplumber


def extrair_conteudo_pdf(caminho: str) -> Optional[str]:
    texto = ""

    try:
        with pdfplumber.open(caminho) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
    except FileNotFoundError:
        print("Arquivo PDF não encontrado.")
        return None
    except PermissionError:
        print("Sem permissão para acessar o PDF.")
        return None
    except OSError as e:
        print(f"Erro de sistema ao ler PDF: {e}")
        return None

    return texto
